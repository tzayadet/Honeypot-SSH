import unittest
from unittest.mock import Mock

import paramiko

from ssh_honeypot import Handler


class HoneypotHandlerTests(unittest.TestCase):
    def test_password_attempt_is_accepted_without_logging_secret(self):
        handler = Handler("192.0.2.10")

        with self.assertLogs("ssh-honeypot", level="INFO") as captured:
            result = handler.check_auth_password("demo-user", "never-log-this-password")

        self.assertEqual(result, paramiko.AUTH_SUCCESSFUL)
        output = "\n".join(captured.output)
        self.assertIn("demo-user", output)
        self.assertIn("192.0.2.10", output)
        self.assertNotIn("never-log-this-password", output)

    def test_only_session_channels_are_allowed(self):
        handler = Handler("192.0.2.10")

        self.assertEqual(handler.check_channel_request("session", 1), paramiko.OPEN_SUCCEEDED)
        self.assertEqual(
            handler.check_channel_request("direct-tcpip", 2),
            paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED,
        )

    def test_interactive_pty_and_shell_are_rejected(self):
        handler = Handler("192.0.2.10")
        channel = Mock()

        self.assertFalse(handler.check_channel_pty_request(channel, "xterm", 80, 24, 0, 0, {}))
        with self.assertLogs("ssh-honeypot", level="INFO"):
            self.assertFalse(handler.check_channel_shell_request(channel))

    def test_exec_request_is_logged_but_never_executed(self):
        handler = Handler("192.0.2.10")
        channel = Mock()

        with self.assertLogs("ssh-honeypot", level="INFO") as captured:
            result = handler.check_channel_exec_request(channel, b"whoami")

        self.assertTrue(result)
        self.assertIn("whoami", "\n".join(captured.output))
        channel.sendall.assert_called_once_with(
            b"Command execution is disabled on this honeypot.\r\n"
        )
        channel.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
