"""
UPSS Tool SDK - Tool Executor

Responsible for executing tools.

Workflow:

Request
    ↓
Registry Lookup
    ↓
Permission Check
    ↓
Execute Tool
    ↓
Return ToolResult
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_result import ToolResult
from tools.tool_schema import ToolInput
from tools.tool_permission import ApprovalStatus

from tools.exceptions import (
    ToolExecutionError,
    ToolNotFoundError,
    ToolPermissionError,
)

from agents.core.tool_registry import ToolRegistry


class ToolExecutor:

    def __init__(self, registry: ToolRegistry):

        self.registry = registry

    async def execute(
        self,
        tool_name: str,
        context: ToolContext,
        request: ToolInput,
        provider: str | None = None,
    ) -> ToolResult:
        """
        Execute a tool by name.
        """

        tool: BaseTool | None = self.registry.get_tool(tool_name)

        #
        # TODO:
        # Resolve provider-specific implementation
        # using ToolRegistry / ProviderFactory.
        #
        _ = provider

        if tool is None:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' not found.",
                tool_name=tool_name,
            )

        permission = tool.permission

        if permission.requires_approval:

            status = context.get(
                "approval_status",
                ApprovalStatus.PENDING,
            )

            if status != ApprovalStatus.APPROVED:

                raise ToolPermissionError(
                    permission.approval_message
                    or f"Approval required for '{tool_name}'.",
                    tool_name=tool_name,
                )

        try:

            result = await tool(
                context=context,
                request=request,
            )

            return result

        except Exception as exc:

            raise ToolExecutionError(
                str(exc),
                tool_name=tool_name,
            ) from exc