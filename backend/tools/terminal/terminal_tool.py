"""
UPSS Terminal Tool

Executes validated terminal commands.
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.terminal.schemas import (
    TerminalRequest,
)

from tools.terminal.command_validator import (
    CommandValidator,
)

from tools.terminal.process_manager import (
    ProcessManager,
)

from tools.terminal.output_parser import (
    OutputParser,
)


class TerminalTool(BaseTool):
    """
    Execute terminal commands after validation.
    """

    metadata = ToolMetadata(
        name="terminal.execute",
        display_name="Terminal",
        description="Execute validated terminal commands.",
        category=ToolCategory.TERMINAL,
        tags=[
            "terminal",
            "shell",
            "powershell",
            "cmd",
            "bash",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = TerminalRequest

    async def execute(
        self,
        context: ToolContext,
        request: TerminalRequest,
    ) -> ToolResult:

        # -----------------------------------------
        # Validate command
        # -----------------------------------------

        valid, message = CommandValidator.validate(
            request.command
        )

        if not valid:

            return ToolResult.failure(
                message=message,
            )

        # -----------------------------------------
        # Validate working directory
        # -----------------------------------------

        valid, message = (
            CommandValidator.validate_working_directory(
                request.working_directory,
            )
        )

        if not valid:

            return ToolResult.failure(
                message=message,
            )

        # -----------------------------------------
        # Execute command
        # -----------------------------------------

        response = await ProcessManager.execute(
            request
        )

        # -----------------------------------------
        # Parse output
        # -----------------------------------------

        parsed = OutputParser.parse(
            response
        )

        # -----------------------------------------
        # Return
        # -----------------------------------------

        if response.success:

            return ToolResult.ok(
                message=parsed["summary"],
                data=parsed,
            )

        return ToolResult.failure(
            message=parsed["summary"],
            data=parsed,
        )