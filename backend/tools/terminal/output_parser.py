"""
UPSS Terminal Output Parser

Parses terminal execution results into a structured format.
"""

from __future__ import annotations

from tools.terminal.schemas import TerminalResponse


class OutputParser:
    """
    Parse terminal output for easier consumption by the LLM.
    """

    WARNING_KEYWORDS = (
        "warning",
        "warn",
        "deprecated",
    )

    ERROR_KEYWORDS = (
        "error",
        "exception",
        "failed",
        "fatal",
        "traceback",
    )

    @classmethod
    def parse(
        cls,
        response: TerminalResponse,
    ) -> dict:

        stdout = response.stdout.strip()
        stderr = response.stderr.strip()

        warnings = []
        errors = []

        # -----------------------------
        # Parse stdout
        # -----------------------------

        for line in stdout.splitlines():

            lower = line.lower()

            if any(word in lower for word in cls.WARNING_KEYWORDS):

                warnings.append(line)

        # -----------------------------
        # Parse stderr
        # -----------------------------

        for line in stderr.splitlines():

            lower = line.lower()

            if any(word in lower for word in cls.ERROR_KEYWORDS):

                errors.append(line)

        return {

            "success": response.success,

            "command": response.command,

            "exit_code": response.exit_code,

            "stdout": stdout,

            "stderr": stderr,

            "warnings": warnings,

            "errors": errors,

            "summary": cls.build_summary(
                response,
                warnings,
                errors,
            ),
        }

    @staticmethod
    def build_summary(
        response: TerminalResponse,
        warnings: list[str],
        errors: list[str],
    ) -> str:

        if response.success:

            if warnings:

                return (
                    f"Command completed successfully "
                    f"with {len(warnings)} warning(s)."
                )

            return "Command executed successfully."

        if errors:

            return (
                f"Command failed with "
                f"{len(errors)} error(s)."
            )

        return "Command execution failed."