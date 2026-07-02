"""
Fallback Selector

Responsibilities

- Select backup tools
- Select backup providers
- Handle unavailable tools

Future

- Provider Health Monitoring
- Reflection Feedback
- Dynamic Failover
- Cost-aware Failover
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class FallbackSelector:

    """
    Handles fallback tool/provider selection.
    """

    # =====================================================
    # Tool Fallback
    # =====================================================

    def select_tool(

        self,

        candidates: List[Dict[str, Any]],

        failed_tool: str,

    ) -> Optional[Dict[str, Any]]:

        for tool in candidates:

            if tool["name"] != failed_tool:

                return tool

        return None

    # =====================================================
    # Provider Fallback
    # =====================================================

    def select_provider(

        self,

        providers: List[str],

        failed_provider: str,

    ) -> Optional[str]:

        for provider in providers:

            if provider != failed_provider:

                return provider

        return None

    # =====================================================
    # Has Tool Fallback
    # =====================================================

    def has_tool_fallback(

        self,

        candidates: List[Dict[str, Any]],

    ) -> bool:

        return len(candidates) > 1

    # =====================================================
    # Has Provider Fallback
    # =====================================================

    def has_provider_fallback(

        self,

        providers: List[str],

    ) -> bool:

        return len(providers) > 1