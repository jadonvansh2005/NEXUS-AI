"""
UPSS Process Manager

Handles asynchronous execution of terminal commands.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from tools.terminal.schemas import (
    TerminalRequest,
    TerminalResponse,
    ShellType,
)


class ProcessManager:
    """
    Executes terminal commands asynchronously.
    """

    @staticmethod
    async def execute(
        request: TerminalRequest,
    ) -> TerminalResponse:

        cwd = (
            Path(request.working_directory).resolve()
            if request.working_directory
            else None
        )

        if request.shell == ShellType.POWERSHELL:

            executable = "powershell"

            args = [
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                request.command,
            ]

        elif request.shell == ShellType.CMD:

            executable = "cmd"

            args = [
                "/c",
                request.command,
            ]

        else:

            executable = "bash"

            args = [
                "-c",
                request.command,
            ]

        process = await asyncio.create_subprocess_exec(

            executable,

            *args,

            cwd=str(cwd) if cwd else None,

            stdout=asyncio.subprocess.PIPE,

            stderr=asyncio.subprocess.PIPE,

        )

        try:

            stdout, stderr = await asyncio.wait_for(

                process.communicate(),

                timeout=request.timeout,

            )

        except asyncio.TimeoutError:

            process.kill()

            await process.wait()

            return TerminalResponse(

                success=False,

                command=request.command,

                exit_code=-1,

                stdout="",

                stderr="Process timed out.",

            )

        return TerminalResponse(

            success=process.returncode == 0,

            command=request.command,

            exit_code=process.returncode,

            stdout=stdout.decode(
                "utf-8",
                errors="replace",
            ),

            stderr=stderr.decode(
                "utf-8",
                errors="replace",
            ),

        )