---
name: no-docker-socket-access
version: "1.0.0"
domain: sectors/cybersecurity
description: Block access to Docker/Podman socket which grants root-equivalent privileges
schema_version: 1
match:
  actions: ["execute", "read", "create"]
  contexts:
    content_pattern: "docker\\.sock|podman\\.sock|containerd\\.sock|var\\/run\\/docker|var\\/run\\/podman|docker.*exec|docker.*run.*-v.*\\/:\\/|--mount.*type=bind.*source=\\/"
verdict: DENY
severity: CRITICAL
priority: 400
author: sovraine
license: CC-BY-SA-4.0
tags: [docker, podman, container-escape, privilege-escalation, socket]
signature: null
certified: false
---

## What it does

Blocks any action that accesses the Docker or Podman socket, or that uses container commands to mount the host filesystem.

## Why it exists

Access to the container runtime socket is equivalent to root access on the host:

- `docker run -v /:/host ubuntu cat /host/etc/shadow` → read any file as root
- `docker exec -it <container> sh` → shell into any running container
- `curl --unix-socket /var/run/docker.sock http://localhost/containers/json` → list all containers
- `docker run --privileged -v /:/host chroot /host` → full root shell on host

In the nirholas attack:
- `docker/docker-compose.yml` mounts `claude-data` volume for persistence
- The Docker configuration is designed to be deployed as a service → persistent C2
- If the container runtime socket were accessible, the RAT could escape the container

## What gets blocked

- `execute` — any command accessing `docker.sock`, `podman.sock`, `containerd.sock`
- `execute` — `docker run` with host filesystem mounts (`-v /:/host`)
- `execute` — `docker exec` into running containers
- `read` — reading socket files
- `create` — mounting socket files into containers

## What is still allowed

- Building container images (`docker build`, `podman build`)
- Running containers with no host mounts and no socket access
- Container operations through the operator's authorized CI/CD pipeline

## How to override

The operator must configure a container operations policy in the gateway specifying allowed Docker/Podman commands, permitted volume mounts, and authorized container images. Socket access is never permitted from repository context. CI/CD pipelines requiring socket access must use a dedicated service account with scoped permissions.
