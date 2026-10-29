import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp_servers.development import core
from mcp_servers.development.core import DevelopmentError


class DevelopmentCoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name).resolve()
        (self.repo / ".git").mkdir()
        self.env = patch.dict(
            os.environ,
            {"NEXUS_DEV_REPO": str(self.repo)},
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        self.addCleanup(self.tmp.cleanup)

    def mock_success(self, stdout="", stderr="", returncode=0):
        return subprocess.CompletedProcess(
            args=["git"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    def test_git_status_uses_configured_repository(self):
        with patch(
            "mcp_servers.development.core.subprocess.run",
            return_value=self.mock_success(" M example.py\n"),
        ) as run:
            result = core.git_status()

        self.assertEqual(result["returncode"], 0)
        self.assertIn("example.py", result["stdout"])
        self.assertEqual(result["repository"], str(self.repo))
        args = run.call_args.args[0]
        self.assertEqual(args[:3], ["git", "-C", str(self.repo)])
        self.assertFalse(run.call_args.kwargs["shell"])

    def test_git_diff_staged_argument(self):
        with patch(
            "mcp_servers.development.core.subprocess.run",
            return_value=self.mock_success(),
        ) as run:
            core.git_diff(staged=True)

        self.assertIn("--cached", run.call_args.args[0])

    def test_git_diff_rejects_non_boolean_staged(self):
        with self.assertRaises(DevelopmentError):
            core.git_diff(staged="yes")

    def test_git_log_rejects_invalid_limits(self):
        for limit in (0, 51, -1, True, "3"):
            with self.subTest(limit=limit):
                with self.assertRaises(DevelopmentError):
                    core.git_log(limit=limit)

    def test_timeout_bounds_are_validated(self):
        with self.assertRaises(DevelopmentError):
            core._run_git(["status"], timeout=0)

        with self.assertRaises(DevelopmentError):
            core._run_git(["status"], timeout=61)

    def test_subprocess_timeout_is_handled(self):
        with patch(
            "mcp_servers.development.core.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="git", timeout=1),
        ):
            with self.assertRaises(DevelopmentError):
                core._run_git(["status"], timeout=1)

    def test_output_is_truncated(self):
        large_output = "x" * (core.MAX_OUTPUT_CHARS + 100)

        with patch(
            "mcp_servers.development.core.subprocess.run",
            return_value=self.mock_success(stdout=large_output),
        ):
            result = core.git_status()

        self.assertEqual(len(result["stdout"]), core.MAX_OUTPUT_CHARS)
        self.assertTrue(result["stdout_truncated"])

    def test_stderr_is_truncated(self):
        large_error = "e" * (core.MAX_OUTPUT_CHARS + 100)

        with patch(
            "mcp_servers.development.core.subprocess.run",
            return_value=self.mock_success(stderr=large_error, returncode=1),
        ):
            result = core.git_status()

        self.assertEqual(len(result["stderr"]), core.MAX_OUTPUT_CHARS)
        self.assertTrue(result["stderr_truncated"])
        self.assertEqual(result["returncode"], 1)

    def test_rejects_non_repository_directory(self):
        with tempfile.TemporaryDirectory() as other:
            with patch.dict(os.environ, {"NEXUS_DEV_REPO": other}):
                with self.assertRaises(DevelopmentError):
                    core.configured_repo()

    def test_git_command_is_anchored_to_configured_repository(self):
        with tempfile.TemporaryDirectory() as other:
            other_repo = Path(other).resolve()
            (other_repo / ".git").mkdir()

            with patch(
                "mcp_servers.development.core.subprocess.run",
                return_value=self.mock_success(),
            ) as run:
                result = core.git_status()

            command = run.call_args.args[0]
            self.assertEqual(command[1], "-C")
            self.assertEqual(Path(command[2]), self.repo)
            self.assertNotEqual(Path(command[2]), other_repo)
            self.assertEqual(result["repository"], str(self.repo))

    def test_output_and_timeout_configuration(self):
        with patch(
            "mcp_servers.development.core.subprocess.run",
            return_value=self.mock_success(),
        ) as run:
            core.git_status()

        kwargs = run.call_args.kwargs
        self.assertTrue(kwargs["capture_output"])
        self.assertTrue(kwargs["text"])
        self.assertEqual(kwargs["timeout"], core.DEFAULT_TIMEOUT_SECONDS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
