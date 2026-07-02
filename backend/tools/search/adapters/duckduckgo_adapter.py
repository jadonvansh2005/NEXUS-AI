"""
UPSS Search - DuckDuckGo Adapter

Currently a placeholder implementation.

Will later use DDGS package.
"""

from __future__ import annotations

from tools.search.adapters.base_adapter import BaseSearchAdapter
from tools.search.schemas import (
    SearchProvider,
    SearchRequest,
    SearchResponse,
)


class DuckDuckGoAdapter(BaseSearchAdapter):

    @property
    def provider_name(self) -> str:
        return SearchProvider.DUCKDUCKGO.value

    async def initialize(self):
        pass

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        raise NotImplementedError(
            "DuckDuckGo adapter is not implemented yet."
        )

    async def close(self):
        pass