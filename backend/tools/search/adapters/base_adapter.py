"""
UPSS Search Adapter Base

Every search provider (Tavily, SerpAPI, Brave, DuckDuckGo)
must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from tools.search.schemas import (
    SearchRequest,
    SearchResponse,
)


class BaseSearchAdapter(ABC):
    """
    Base class for all search providers.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Provider identifier.

        Example:
            tavily
            serpapi
            brave
        """
        raise NotImplementedError

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize provider.

        Load API Keys
        Create HTTP Session
        etc.
        """
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:
        """
        Execute search.
        """
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """
        Cleanup resources.
        """
        raise NotImplementedError