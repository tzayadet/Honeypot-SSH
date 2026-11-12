#!/usr/bin/env python3
"""Isolated SSH honeypot for recording authentication metadata and exec attempts.

This service deliberately does not provide a shell or execute submitted commands.
Run it only in an isolated lab network. Password values are never stored or logged.
"""
from __future__ import annotations

import logging
import os
import socket
import threading

import paramiko

LOG_FILE = os.environ.get("HP_LOG_FILE", "hp.log")
HOST = os.environ.get("HP_HOST", "127.0.0.1")
PORT = int(os.environ.get("HP_PORT", "2222"))
MAX_CLIENTS = 32
CLIENT_TIMEOUT_SECONDS = 30
ACTIVE_CLIENTS = threading.BoundedSemaphore(MAX_CLIENTS)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("ssh-honeypot")


class Handler(paramiko.ServerInterface):
    """Record attempted access without exposing a command execution surface."""

    def __init__(self, remote_ip: str) -> None:
        self.remote_ip = remote_ip

    def get_allowed_auths(self, username: str) -> str:
        return "password"

    def check_auth_password(self, username: str, password: str) -> int:
        # Never log, hash, persist, or otherwise retain the supplied password.
        logger.info("AUTH_ATTEMPT | username=%r | ip=%s", username[:128], self.remote_ip)
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        # No interactive terminal is provided.
        return False

    def check_channel_shell_request(self, channel) -> bool:
        # Explicitly refuse interactive shells.
        logger.info("SHELL_REQUEST | ip=%s | result=denied", self.remote_ip)
        return False

    def check_channel_exec_request(self, channel, command: bytes) -> bool:
        # Record the requested command for analysis, but never execute it.
        requested = command.decode("utf-8", errors="replace")[:2048]
        logger.info("EXEC_ATTEMPT | ip=%s | command=%r", self.remote_ip, requested)
        try:
            channel.sendall(b"Command execution is disabled on this honeypot.\r\n")
        finally:
            channel.close()
        return True


def handle_client(client: socket.socket, address: tuple[str, int], host_key: paramiko.PKey) -> None:
    remote_ip = address[0]
    transport = None
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        transport.start_server(server=Handler(remote_ip))
        transport.join()
    except (OSError, paramiko.SSHException) as exc:
        logger.info("CONNECTION_CLOSED | ip=%s | reason=%s", remote_ip, type(exc).__name__)
    finally:
        try:
            if transport is not None:
                transport.close()
            else:
                client.close()
        finally:
            ACTIVE_CLIENTS.release()


def main() -> None:
    host_key = paramiko.RSAKey.generate(2048)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)
        logger.info("HONEYPOT_STARTED | bind=%s | port=%s", HOST, PORT)
        print(f"SSH honeypot listening on {HOST}:{PORT} (no shell, no command execution)")
        while True:
            client, address = server.accept()
            if not ACTIVE_CLIENTS.acquire(blocking=False):
                logger.warning("CONNECTION_REJECTED | ip=%s | reason=capacity", address[0])
                client.close()
                continue
            try:
                client.settimeout(CLIENT_TIMEOUT_SECONDS)
                threading.Thread(
                    target=handle_client,
                    args=(client, address, host_key),
                    daemon=True,
                ).start()
            except Exception:
                ACTIVE_CLIENTS.release()
                client.close()
                raise


if __name__ == "__main__":
    main()
