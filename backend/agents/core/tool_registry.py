"""
Global Tool Registry

Responsibilities

- Register all available tools
- Retrieve tools
- Search by domain
- Search by capability
- Search by provider
- Enable / Disable tools

This is the SINGLE Tool Registry used across UPSS.
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from agents.core.tool_definition import (
    ToolDefinition,
)


class ToolRegistry:

    def __init__(self):

        self.tools: Dict[str, ToolDefinition] = {}
    # =====================================================
    # Register Tool
    # =====================================================

    def register_tool(

        self,

        name: str,

        tool: Any,

        domain: str,

        capabilities: List[str],

        providers: List[str] | None = None,

        enabled: bool = True,

    ) -> None:

        self.tools[name] = ToolDefinition(

            name=name,

            domain=domain,

            capabilities=capabilities,

            providers=providers or [],

            execution_class=tool.__class__.__name__,

            enabled=enabled,

            metadata={

                "instance": tool,

            },

        )

    # =====================================================
    # Get Tool
    # =====================================================

    def get_tool(

        self,

        name: str,

    ) -> Optional[Any]:

        tool = self.tools.get(name)

        if tool is None:

            return None

        return tool.metadata.get(

            "instance"

        )

    # =====================================================
    # Get Tool Metadata
    # =====================================================

    def get_metadata(

        self,

        name: str,

    ) -> Optional[Dict[str, Any]]:

        return self.tools.get(name)

    # =====================================================
    # Has Tool
    # =====================================================

    def has_tool(

        self,

        name: str,

    ) -> bool:

        return name in self.tools

    # =====================================================
    # Remove Tool
    # =====================================================

    def unregister_tool(

        self,

        name: str,

    ) -> None:

        self.tools.pop(

            name,

            None,

        )

    # =====================================================
    # List Tool Names
    # =====================================================

    def list_tools(

        self,

    ) -> List[str]:

        return list(

            self.tools.keys()

        )

    # =====================================================
    # Get All Metadata
    # =====================================================

    def all_tools(

        self,

    ) -> List[Dict[str, Any]]:

        return list(

            self.tools.values()

        )

    # =====================================================
    # Search By Domain
    # =====================================================

    def get_tools_by_domain(

        self,

        domain: str,

    ) -> List[Dict[str, Any]]:

        return [

            tool

            for tool in self.tools.values()

            if tool.domain == domain

            and tool.enabled

        ]

    # =====================================================
    # Search By Capability
    # =====================================================

    def get_tools_by_capability(

        self,

        capability: str,

    ) -> List[Dict[str, Any]]:

        return [

            tool

            for tool in self.tools.values()

            if capability in tool.capabilities

            and tool.enabled

        ]

    # =====================================================
    # Search By Provider
    # =====================================================

    def get_tools_by_provider(

        self,

        provider: str,

    ) -> List[Dict[str, Any]]:

        return [

            tool

            for tool in self.tools.values()

            if provider in tool.providers

            and tool.enabled

        ]

    # =====================================================
    # Enabled Tools
    # =====================================================

    def get_enabled_tools(

        self,

    ) -> List[Dict[str, Any]]:

        return [

            tool

            for tool in self.tools.values()

            if tool.enabled

        ]

    # =====================================================
    # Enable Tool
    # =====================================================

    def enable_tool(

        self,

        name: str,

    ) -> None:

        if name in self.tools:

            self.tools[name].enabled = True

    # =====================================================
    # Disable Tool
    # =====================================================

    def disable_tool(

        self,

        name: str,

    ) -> None:

        if name in self.tools:

            self.tools[name].enabled = False

    # =====================================================
    # Registry Info
    # =====================================================

    def count(

        self,

    ) -> int:

        return len(

            self.tools

        )

    # =====================================================
    # Clear Registry
    # =====================================================

    def clear(

        self,

    ) -> None:

        self.tools.clear()