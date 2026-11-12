<p align="center">
  <img src="https://img.shields.io/badge/DECEPTION_LAB-SSH_HONEYPOT-101010?style=for-the-badge&labelColor=050805&color=00FF41" alt="SSH deception lab"/>
  <img src="https://img.shields.io/badge/PYTHON-PARAMIKO-101010?style=for-the-badge&logo=python&logoColor=00FF41" alt="Python"/>
</p>

# SSH Deception Lab

A low-interaction SSH honeypot prototype built with Python and Paramiko. It records authentication attempts and requested SSH commands for controlled lab analysis without executing submitted commands.

<p align="center">
  <a href="https://tzayadet.github.io/Honeypot-SSH/"><strong>PROJECT SHOWCASE ↗</strong></a> ·
  <a href="https://github.com/tzayadet/Honeypot-SSH"><strong>SOURCE CODE</strong></a>
</p>

[![Python CI](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/container-build.yml)

## Features

- Records usernames and source IP addresses from authentication attempts.
- Does not store, print or log submitted passwords.
- Rejects interactive terminal and shell requests.
- Records SSH `exec` requests without running the submitted commands.
- Supports local execution and Docker-based lab deployment.

## Run locally

**Requirements:** Python 3.11+ and Paramiko 3.5+.

```bash
python -m pip install -r requirements.txt
python ssh_honeypot.py
```

By default, the service listens on loopback at port 2222. Environment variables can configure the bind address, port and log file.

## Docker

```bash
docker build -t ssh-deception-lab .
docker run --rm --name ssh-deception-lab \
  -p 127.0.0.1:2222:2222 \
  -v "$PWD/logs:/app/logs" \
  -e HP_LOG_FILE=/app/logs/hp.log \
  ssh-deception-lab
```

Keep the service bound to loopback or an isolated lab network. Do not publish the container port on a public host interface.

## Project layout

| Path | Purpose |
|---|---|
| `ssh_honeypot.py` | SSH honeypot service |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container build |
| `tests/` | Behaviour and safety tests |
| `.github/workflows/` | Automated checks and showcase deployment |

## Showcase

The [static showcase](https://tzayadet.github.io/Honeypot-SSH/) presents the project and its behaviour. It does not run an SSH service or collect network traffic.

## Scope and safety

This is a low-interaction experimental honeypot, not a production SSH server or an isolated execution environment. It does not provide a fake shell, command execution, session persistence or a complete log-management system.

Run it in a virtual machine or isolated network. Protect collected logs: usernames, source addresses and requested commands may contain sensitive information.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

See [LICENSE](LICENSE).
