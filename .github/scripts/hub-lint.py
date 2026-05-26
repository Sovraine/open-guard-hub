#!/usr/bin/env python3
# SPDX-License-Identifier: CC-BY-SA-4.0
# Copyright (c) 2026 SOVRAINE PTE.LTD. All rights reserved.
"""Hub content security lint — 12 paranoid checks for supply-chain integrity."""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

import yaml

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"::error::{msg}")


def get_changed_files() -> list[str]:
    base = os.environ.get("BASE_SHA", "")
    head = os.environ.get("HEAD_SHA", "HEAD")
    if not base:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        capture_output=True,
        text=True,
    )
    return [f for f in result.stdout.strip().splitlines() if f]


def content_files(extensions: tuple[str, ...] = ("*.yaml", "*.yml", "*.md")) -> list[str]:
    files = []
    for ext in extensions:
        for f in glob.glob(f"**/{ext}", recursive=True):
            if ".git/" not in f:
                files.append(f)
    return files


def check_yaml_bomb() -> None:
    for f in content_files(("*.yaml", "*.yml")):
        size = os.path.getsize(f)
        if size > 1_048_576:
            fail(f"[1/12] YAML bomb: {f} exceeds 1MB ({size} bytes)")


def check_self_certification(changed: list[str]) -> None:
    cert_re = re.compile(r"certified:\s*true|signature:\s*(?!null\b)\S")
    hub_exts = (".guard.md", ".agent.md", ".soul.md", ".skill.md", ".yaml", ".yml")
    for f in changed:
        if any(f.endswith(ext) for ext in hub_exts) and os.path.isfile(f):
            with open(f) as fh:
                if cert_re.search(fh.read()):
                    fail(f"[2/12] Self-certification: {f}")


def check_symlinks() -> None:
    for root, dirs, files in os.walk("."):
        if ".git" in root.split(os.sep):
            continue
        for name in files + dirs:
            path = os.path.join(root, name)
            if os.path.islink(path):
                fail(f"[3/12] Symlink not allowed: {path}")


def check_binary_content() -> None:
    for f in content_files():
        with open(f, "rb") as fh:
            if b"\x00" in fh.read():
                fail(f"[4/12] Binary content (null bytes): {f}")


def check_executable_permissions() -> None:
    for root, _dirs, files in os.walk("."):
        parts = root.split(os.sep)
        if ".git" in parts or ".github" in parts:
            continue
        for name in files:
            path = os.path.join(root, name)
            if os.stat(path).st_mode & 0o111:
                fail(f"[5/12] Executable permission: {path}")


def check_hidden_files() -> None:
    allowed_roots = {".github", ".claude"}
    allowed_files = {".gitignore", ".gitattributes"}
    for root, dirs, files in os.walk("."):
        if ".git" in root.split(os.sep):
            continue
        for name in dirs + files:
            if not name.startswith("."):
                continue
            if name == ".git":
                continue
            if name in allowed_roots or name in allowed_files:
                continue
            path = os.path.join(root, name)
            inside_allowed = any(
                f"/{a}/" in path.replace(os.sep, "/") or path.replace(os.sep, "/").startswith(f"./{a}/")
                for a in allowed_roots
            )
            if not inside_allowed:
                fail(f"[6/12] Hidden file/dir: {path}")


def check_ascii_filenames() -> None:
    for root, dirs, files in os.walk("."):
        if ".git" in root.split(os.sep):
            continue
        for name in files + dirs:
            if not name.isascii():
                fail(f"[7/12] Non-ASCII filename: {os.path.join(root, name)}")


def check_git_config_tampering(changed: list[str]) -> None:
    blocked = {".gitmodules", ".mailmap"}
    for f in changed:
        if os.path.basename(f) in blocked:
            fail(f"[8/12] Git config tampering: {f}")


def check_workflow_isolation(changed: list[str]) -> None:
    workflow_changed = any(f.startswith(".github/workflows/") for f in changed)
    content_changed = any(
        not f.startswith((".", ".github/", ".claude/"))
        for f in changed
    )
    if workflow_changed and content_changed:
        fail("[9/12] Workflow + content changes in same PR — split into separate PRs")


def check_template_injection() -> None:
    template_re = re.compile(r"\$\{\{")
    for f in content_files():
        if ".github/" in f:
            continue
        with open(f) as fh:
            for i, line in enumerate(fh, 1):
                if template_re.search(line):
                    fail(f"[10/12] Template injection (${{{{}}}}): {f}:{i}")


def check_priority_author(changed: list[str]) -> None:
    fm_re = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)
    for f in changed:
        if not f.endswith(".guard.md") or not os.path.isfile(f):
            continue
        with open(f) as fh:
            content = fh.read()
        m = fm_re.search(content)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except yaml.YAMLError:
            fail(f"[11/12] Invalid YAML frontmatter: {f}")
            continue
        if not isinstance(fm, dict):
            continue
        priority = fm.get("priority", 0)
        if isinstance(priority, int) and priority > 500:
            fail(f"[11/12] Priority too high: {f} ({priority}, max 500 for community)")
        author = fm.get("author")
        if author is not None and author != "community":
            fail(f"[11/12] Invalid author: {f} ('{author}', must be 'community')")


def check_yaml_anchors_depth() -> None:
    anchor_re = re.compile(r"&\w+")
    alias_re = re.compile(r"\*\w+")
    for f in content_files(("*.yaml", "*.yml")):
        with open(f) as fh:
            content = fh.read()
        anchors = anchor_re.findall(content)
        aliases = alias_re.findall(content)
        if len(anchors) > 20:
            fail(f"[12/12] Excessive YAML anchors: {f} ({len(anchors)}, max 20)")
        if len(aliases) > 50:
            fail(f"[12/12] Excessive YAML aliases: {f} ({len(aliases)}, max 50)")
        lines = [line for line in content.splitlines() if line.strip()]
        if lines:
            max_indent = max(len(line) - len(line.lstrip()) for line in lines)
            if max_indent > 40:
                fail(f"[12/12] YAML nesting too deep: {f} ({max_indent} spaces indent, max 40)")


def main() -> None:
    changed = get_changed_files()
    print(f"Changed files: {len(changed)}")

    check_yaml_bomb()
    check_self_certification(changed)
    check_symlinks()
    check_binary_content()
    check_executable_permissions()
    check_hidden_files()
    check_ascii_filenames()
    check_git_config_tampering(changed)
    check_workflow_isolation(changed)
    check_template_injection()
    check_priority_author(changed)
    check_yaml_anchors_depth()

    if errors:
        print(f"\n{len(errors)} security issue(s) found.")
        sys.exit(1)
    print("\n12/12 checks passed.")


if __name__ == "__main__":
    main()
