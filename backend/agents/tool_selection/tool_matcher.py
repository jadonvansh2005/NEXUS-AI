"""
Tool Matcher

Responsibilities

- Match capabilities to candidate tools
- Query Tool Registry
- Return candidate tools

Future

- Semantic capability matching
- Vector search
- MCP discovery
- External tool discovery
"""

from __future__ import annotations

from typing import List
from typing import Dict
from typing import Any

from agents.core.tool_registry import (
    ToolRegistry,
)


class ToolMatcher:

    """
    Finds candidate tools for a capability.
    """

    def __init__(

        self,

        registry: ToolRegistry,

    ):

        self.registry = registry

    # =====================================================
    # Match
    # =====================================================

    def match(

        self,

        capabilities: List[str],

    ) -> List[Dict[str, Any]]:

        candidates: List[Dict[str, Any]] = []

        seen = set()

        for capability in capabilities:

            tools = (

                self.registry.get_tools_by_capability(

                    capability

                )

            )

            for tool in tools:

                if tool.name not in seen:

                    candidates.append(

                        tool

                    )

                    seen.add(

                        tool.name

                    )

        return candidates

    # =====================================================
    # Domain Match
    # =====================================================

    def match_domain(

        self,

        domain: str,

    ) -> List[Dict[str, Any]]:

        return (

            self.registry.get_tools_by_domain(

                domain

            )

        )

    # =====================================================
    # Provider Match
    # =====================================================

    def match_provider(

        self,

        provider: str,

    ) -> List[Dict[str, Any]]:

        return (

            self.registry.get_tools_by_provider(

                provider

            )

        )