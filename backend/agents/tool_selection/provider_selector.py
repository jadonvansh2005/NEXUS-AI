"""
Provider Selector

Responsibilities

- Select the best provider for a tool
- Handle provider priority
- Support provider failover

Future

- Health Checks
- Latency Monitoring
- Cost Optimization
- Geographic Routing
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from agents.core.tool_definition import (
    ToolDefinition,
)

from agents.tool_selection.provider_registry import (
    ProviderRegistry,
)

class ProviderSelector:

    """
    Selects the best provider for a tool.
    """

    def __init__(

        self,

        provider_registry: ProviderRegistry,

    ):

        self.provider_registry = (

            provider_registry

        )

    # =====================================================
    # Public API
    # =====================================================

    def select(

        self,

        tool: ToolDefinition,

    ) -> Optional[str]:

        providers = (

            self.provider_registry.get_providers(

                tool.name

            )

        )

        if not providers:

            return None

        return self.provider_registry.get_default_provider(

            tool.name

        )

    # =====================================================
    # Get All Providers
    # =====================================================

    def available_providers(

        self,

        tool: ToolDefinition,

    ) -> List[str]:

        return self.provider_registry.get_providers(

            tool.name

        )

    # =====================================================
    # Has Provider
    # =====================================================

    def has_provider(

        self,

        tool: ToolDefinition,

        provider: str,

    ) -> bool:

        return self.provider_registry.has_provider(

            tool.name,

            provider,

        )