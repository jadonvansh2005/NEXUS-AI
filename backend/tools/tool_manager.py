"""
UPSS Tool SDK - Tool Manager

High-level interface for the Tool SDK.

Coordinates:
    - Tool Discovery
    - Tool Registry
    - Tool Execution
"""

from __future__ import annotations

from agents.core.tool_registry import ToolRegistry

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_discovery import ToolDiscovery
from tools.tool_executor import ToolExecutor
from tools.tool_result import ToolResult
from tools.tool_schema import ToolInput

from agents.tool_selection.provider_registry import (
    ProviderRegistry,
)


class ToolManager:

    def __init__(self, registry: ToolRegistry):

        self.registry = registry

        self.provider_registry = (

            ProviderRegistry()

        )

        self.discovery = (

            ToolDiscovery(

                registry,

                self.provider_registry,

            )

        )
        self.executor = ToolExecutor(registry)


    # -----------------------------------------------------
    # Initialize
    # -----------------------------------------------------

    def initialize(

        self,

    ) -> None:

        """
        Discover and register all tools.
        Should be called once during application startup.
        """

        self.discover_tools()

    # -----------------------------------------------------
    # Discovery
    # -----------------------------------------------------

    def discover_tools(self) -> int:
        """
        Discover and register all tools.
        """

        return self.discovery.discover()

    # -----------------------------------------------------
    # Registry Helpers
    # -----------------------------------------------------

    def get_tool(self, tool_name: str) -> BaseTool | None:
        """
        Get a registered tool.
        """

        return self.registry.get_tool(tool_name)

    def list_tools(self):

        return self.registry.list_tools()

    def has_tool(self, tool_name: str) -> bool:

        return self.registry.has_tool(tool_name)

    # -----------------------------------------------------
    # Execution
    # -----------------------------------------------------

    async def execute(
        self,
        tool_name: str,
        context: ToolContext,
        request: ToolInput,
    ) -> ToolResult:
        """
        Execute a tool.
        """

        return await self.executor.execute(
            tool_name=tool_name,
            context=context,
            request=request,
        )