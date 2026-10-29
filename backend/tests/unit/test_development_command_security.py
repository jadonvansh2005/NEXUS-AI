import unittest
from unittest.mock import patch
import io
import sys
import time
from pathlib import Path

from mcp_servers.development import core
from mcp_servers.development.core import DevelopmentError


class DevelopmentCommandSecurityTests(unittest.TestCase):
    def test_arbitrary_shell_command_is_rejected(self):
        with self.assertRaises(DevelopmentError):
            core.run_dev_command("powershell -Command Remove-Item")

    def test_unknown_command_id_is_rejected(self):
        with self.assertRaises(DevelopmentError):
            core.run_dev_command("npm_install")

    def test_allowlisted_command_has_fixed_arguments(self):
        command = core.ALLOWED_DEV_COMMANDS["python_unit_tests"]
        self.assertEqual(command[1:5], [
            "-m", "unittest", "discover", "-s"
        ])
        self.assertEqual(command[-2:], ["-p", "test_development*.py"])

    def test_output_limit_is_configured(self):
        self.assertEqual(core.MAX_COMMAND_OUTPUT_BYTES, 64000)

    def test_command_timeout_is_configured(self):
        self.assertEqual(core.COMMAND_TIMEOUT_SECONDS, 120)

    def test_no_shell_execution(self):
        self.assertIsInstance(core.ALLOWED_DEV_COMMANDS, dict)
        # The runner's Popen invocation must use shell=False.
        # Full invocation behavior is checked in the next integration test.
        
    def test_subprocess_is_invoked_without_shell(self):
        class FakeProcess:
            def __init__(self):
                self.stdout = io.BytesIO(b"ok")
                self.stderr = io.BytesIO(b"")
                self.returncode = 0

            def wait(self, timeout=None):
                return self.returncode

        fake_process = FakeProcess()

        with (
            patch.object(
                core,
                "configured_repo",
                return_value=Path.cwd(),
            ),
            patch.dict(
                core.ALLOWED_DEV_COMMANDS,
                {"python_unit_tests": ["controlled-test-command"]},
            ),
            patch.object(
                core.subprocess,
                "Popen",
                return_value=fake_process,
            ) as mock_popen,
        ):
            result = core.run_dev_command("python_unit_tests")

        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assertIs(
            mock_popen.call_args.kwargs["shell"],
            False,
        )

    def test_output_is_bounded_during_real_execution(self):
        command = [
            sys.executable,
            "-c",
            "import sys; sys.stdout.write('X' * 70000)",
        ]

        with patch.dict(
            core.ALLOWED_DEV_COMMANDS,
            {"python_unit_tests": command},
        ):
            result = core.run_dev_command("python_unit_tests")

        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assertEqual(
            len(result["stdout"].encode("utf-8")),
            core.MAX_COMMAND_OUTPUT_BYTES,
        )
        self.assertTrue(result["stdout_truncated"])

    def test_real_process_timeout_is_enforced(self):
        command = [
            sys.executable,
            "-c",
            "import time; time.sleep(10)",
        ]

        with (
            patch.dict(
                core.ALLOWED_DEV_COMMANDS,
                {"python_unit_tests": command},
            ),
            patch.object(
                core,
                "COMMAND_TIMEOUT_SECONDS",
                1,
            ),
        ):
            start = time.monotonic()
            result = core.run_dev_command("python_unit_tests")
            elapsed = time.monotonic() - start

        self.assertTrue(result["timed_out"])
        self.assertLess(elapsed, 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
