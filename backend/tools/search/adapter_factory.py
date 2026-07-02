"""
UPSS Search Adapter Factory

Responsible for creating and managing search adapters.
"""

from __future__ import annotations

from typing import Dict, Type

from tools.search.schemas import SearchProvider
from tools.search.adapters.base_adapter import BaseSearchAdapter

from tools.search.adapters.tavily_adapter import TavilyAdapter
from tools.search.adapters.serpapi_adapter import SerpAPIAdapter
from tools.search.adapters.duckduckgo_adapter import DuckDuckGoAdapter


class SearchAdapterFactory:
    """
    Factory responsible for creating search adapters.

    Supports:
        - Tavily
        - SerpAPI
        - DuckDuckGo

    New providers can be registered without modifying
    WebSearchTool.
    """

    _registry: Dict[
        SearchProvider,
        Type[BaseSearchAdapter]
    ] = {

        SearchProvider.TAVILY: TavilyAdapter,

        SearchProvider.SERPAPI: SerpAPIAdapter,

        SearchProvider.DUCKDUCKGO: DuckDuckGoAdapter,

    }

    @classmethod
    def register(
        cls,
        provider: SearchProvider,
        adapter: Type[BaseSearchAdapter],
    ) -> None:
        """
        Register a new adapter.
        """

        cls._registry[provider] = adapter

    @classmethod
    def create(
        cls,
        provider: SearchProvider = SearchProvider.AUTO,
    ) -> BaseSearchAdapter:
        """
        Create adapter instance.

        AUTO currently defaults to Tavily.
        """

        if provider == SearchProvider.AUTO:
            provider = SearchProvider.TAVILY

        adapter_cls = cls._registry.get(provider)

        if adapter_cls is None:
            raise ValueError(
                f"No adapter registered for provider '{provider.value}'."
            )

        return adapter_cls()

    @classmethod
    def supported_providers(
        cls,
    ) -> list[SearchProvider]:
        """
        Return all supported providers.
        """

        return list(cls._registry.keys())

    @classmethod
    def is_supported(
        cls,
        provider: SearchProvider,
    ) -> bool:
        """
        Check whether provider is supported.
        """

        return provider in cls._registry