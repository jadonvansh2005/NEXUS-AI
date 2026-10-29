from __future__ import annotations

import os
import subprocess
from pathlib import Path
import sys
import threading
import time

DEFAULT_REPO = Path(r"D:\UPSS").resolve()
MAX_OUTPUT_CHARS = 20_000
DEFAULT_TIMEOUT_SECONDS = 15
MAX_TIMEOUT_SECONDS = 60


class DevelopmentError(ValueError):
    """Safe, user-facing development tool error."""


def configured_repo() -> Path:
    raw = os.environ.get("NEXUS_DEV_REPO", str(DEFAULT_REPO)).strip()
    if not raw:
        raise DevelopmentError("NEXUS_DEV_REPO cannot be empty.")

    try:
        repo = Path(raw).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise DevelopmentError("Configured repository does not exist.") from exc

    if not repo.is_dir():
        raise DevelopmentError("Configured repository must be a directory.")

    if not (repo / ".git").exists():
        raise DevelopmentError("Configured directory is not a Git repository.")

    return repo


def _run_git(
    args: list[str],
    *,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict:
    if not isinstance(args, list) or not args:
        raise DevelopmentError("A Git argument list is required.")

    if not 1 <= timeout <= MAX_TIMEOUT_SECONDS:
        raise DevelopmentError(
            f"Timeout must be between 1 and {MAX_TIMEOUT_SECONDS} seconds."
        )

    repo = configured_repo()

    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            shell=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise DevelopmentError("Git command timed out.") from exc
    except OSError as exc:
        raise DevelopmentError("Could not execute Git.") from exc

    return {
        "repository": str(repo),
        "command": ["git", *args],
        "returncode": result.returncode,
        "stdout": result.stdout[:MAX_OUTPUT_CHARS],
        "stderr": result.stderr[:MAX_OUTPUT_CHARS],
        "stdout_truncated": len(result.stdout) > MAX_OUTPUT_CHARS,
        "stderr_truncated": len(result.stderr) > MAX_OUTPUT_CHARS,
    }


def git_status() -> dict:
    """Return concise Git working-tree status."""
    return _run_git(["status", "--short"])


def git_diff(staged: bool = False) -> dict:
    """Return a bounded diff; staged=True inspects staged changes."""
    if not isinstance(staged, bool):
        raise DevelopmentError("staged must be a boolean.")

    args = ["diff", "--no-ext-diff", "--no-color"]
    if staged:
        args.append("--cached")

    return _run_git(args)


def git_log(limit: int = 10) -> dict:
    """Return recent commit summaries."""
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 50:
        raise DevelopmentError("limit must be an integer between 1 and 50.")

    return _run_git([
        "log",
        f"-{limit}",
        "--date=iso-strict",
        "--format=%h %ad %s",
    ])


MAX_COMMAND_OUTPUT_BYTES = 64_000
COMMAND_TIMEOUT_SECONDS = 120

ALLOWED_DEV_COMMANDS = {
    "python_unit_tests": [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "backend/tests/unit",
        "-p",
        "test_development*.py",
    ],
}


def _read_bounded_stream(stream, output, limit):
    """Drain a process stream while retaining at most limit bytes."""
    try:
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            remaining = limit - len(output)
            if remaining > 0:
                output.extend(chunk[:remaining])
    finally:
        stream.close()


def run_dev_command(command_id: str) -> dict:
    """Run one predefined development command in the configured repository."""
    if not isinstance(command_id, str):
        raise DevelopmentError("command_id must be a string.")

    if command_id not in ALLOWED_DEV_COMMANDS:
        raise DevelopmentError("Command is not in the development allowlist.")

    repo = configured_repo()
    command = ALLOWED_DEV_COMMANDS[command_id]

    env = os.environ.copy()
    backend_dir = repo / "backend"
    if backend_dir.is_dir():
        env["PYTHONPATH"] = str(backend_dir)

    try:
        process = subprocess.Popen(
            command,
            cwd=str(repo),
            env=env,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        raise DevelopmentError("Could not start the allowed command.") from exc

    stdout_bytes = bytearray()
    stderr_bytes = bytearray()

    stdout_thread = threading.Thread(
        target=_read_bounded_stream,
        args=(process.stdout, stdout_bytes, MAX_COMMAND_OUTPUT_BYTES),
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=_read_bounded_stream,
        args=(process.stderr, stderr_bytes, MAX_COMMAND_OUTPUT_BYTES),
        daemon=True,
    )
    stdout_thread.start()
    stderr_thread.start()

    timed_out = False
    try:
        process.wait(timeout=COMMAND_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()

    stdout_thread.join()
    stderr_thread.join()

    return {
        "command_id": command_id,
        "returncode": process.returncode,
        "timed_out": timed_out,
        "stdout": stdout_bytes.decode("utf-8", errors="replace"),
        "stderr": stderr_bytes.decode("utf-8", errors="replace"),
        "stdout_truncated": len(stdout_bytes) >= MAX_COMMAND_OUTPUT_BYTES,
        "stderr_truncated": len(stderr_bytes) >= MAX_COMMAND_OUTPUT_BYTES,
    }

