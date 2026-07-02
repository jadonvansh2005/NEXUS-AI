"""
UPSS Command Validator

Validates terminal commands before execution.
"""

from __future__ import annotations

from pathlib import Path


class CommandValidator:
    """
    Validate terminal commands before execution.
    """

    # Dangerous commands
    BLOCKED_COMMANDS = {

        # Windows
        "format",
        "diskpart",
        "shutdown",
        "restart-computer",
        "stop-computer",
        "Remove-Computer",

        # Linux
        "rm -rf /",
        "mkfs",
        "reboot",
        "shutdown",

        # Generic
        "del /f /s /q",
        "cipher /w",
    }

    @classmethod
    def validate(
        cls,
        command: str,
    ) -> tuple[bool, str]:

        command = command.strip()

        if not command:
            return False, "Empty command."

        lower = command.lower()

        for blocked in cls.BLOCKED_COMMANDS:

            if blocked.lower() in lower:

                return (
                    False,
                    f"Blocked command detected: {blocked}",
                )

        return True, ""

    @staticmethod
    def validate_working_directory(
        directory: str | None,
    ) -> tuple[bool, str]:

        if directory is None:
            return True, ""

        path = Path(directory)

        if not path.exists():

            return (
                False,
                f"Directory does not exist: {directory}",
            )

        if not path.is_dir():

            return (
                False,
                f"Not a directory: {directory}",
            )

        return True, ""