"""
Provider Registry

Responsibilities

- Register providers for tools
- Retrieve providers
- Maintain provider priorities
- Maintain default providers

Single source of truth for provider information.
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional


class ProviderRegistry:

    """
    Registry containing provider information
    for every registered tool.
    """

    def __init__(self):

        self._providers: Dict[str, List[str]] = {}

    # =====================================================
    # Register
    # =====================================================

    def register(

        self,

        tool_name: str,

        providers: List[str],

    ) -> None:

        self._providers[tool_name] = list(

            dict.fromkeys(

                providers

            )

        )

    # =====================================================
    # Get Providers
    # =====================================================

    def get_providers(

        self,

        tool_name: str,

    ) -> List[str]:

        return self._providers.get(

            tool_name,

            [],

        )

    # =====================================================
    # Default Provider
    # =====================================================

    def get_default_provider(

        self,

        tool_name: str,

    ) -> Optional[str]:

        providers = self.get_providers(

            tool_name

        )

        if not providers:

            return None

        return providers[0]

    # =====================================================
    # Has Provider
    # =====================================================

    def has_provider(

        self,

        tool_name: str,

        provider: str,

    ) -> bool:

        return provider in self.get_providers(

            tool_name

        )

    # =====================================================
    # Remove
    # =====================================================

    def unregister(

        self,

        tool_name: str,

    ) -> None:

        self._providers.pop(

            tool_name,

            None,

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(

        self,

    ) -> None:

        self._providers.clear()