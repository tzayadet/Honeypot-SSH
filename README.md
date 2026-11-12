# SSH Deception Lab

A Python-based SSH honeypot prototype built with Paramiko. It records authentication attempts and requested SSH commands for controlled lab analysis without executing submitted commands.

<p align="center">
  <a href="https://tzayadet.github.io/Honeypot-SSH/"><img src="https://img.shields.io/badge/LIVE_SHOWCASE-OPEN-00a86b?style=flat-square" alt="Live showcase"></a>
  <a href="https://github.com/tzayadet/Honeypot-SSH"><img src="https://img.shields.io/badge/SOURCE-GITHUB-161b22?style=flat-square&logo=github" alt="Source code"></a>
</p>

[![Python CI](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Honeypot-SSH/actions/workflows/container-build.yml)

## What it does

- Records usernames and source IP addresses from authentication attempts.
- Does not store, print or log submitted passwords.
- Rejects interactive terminal and shell requests.
- Records SSH `exec` requests without running the submitted commands.
- Supports local execution and Docker-based lab deployment.

## Run locally

**Requirements:** Python 3.11 or later and Paramiko 3.5 or later.

```bash
python -m pip install -r requirements.txt
python ssh_honeypot.py
```

By default, the service listens on loopback at port 2222. Environment variables can be used to configure the bind address, port and log file.

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

## Project structure

| Path | Purpose |
|---|---|
| `ssh_honeypot.py` | SSH honeypot service |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container build |
| `tests/` | Behaviour and safety tests |
| `.github/workflows/` | Automated checks and showcase deployment |

## Live showcase

[Open SSH Deception Lab](https://tzayadet.github.io/Honeypot-SSH/)

The static page presents the project and its behaviour. It does not run an SSH service or collect network traffic.

## Scope and safety

This is a low-interaction experimental honeypot, not a production SSH server or an isolated execution environment. It does not provide a fake shell, command execution, session persistence or a complete log-management system. Run it in a virtual machine or isolated network and protect collected logs: usernames, source addresses and requested commands may contain sensitive information.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

See [LICENSE](LICENSE) for the repository's licensing terms.
