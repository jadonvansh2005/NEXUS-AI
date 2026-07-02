"""
UPSS Search - SerpAPI Adapter
"""

from __future__ import annotations

import os

from tools.http.auth import APIKeyAuth
from tools.http.http_client import HTTPClient

from tools.search.adapters.base_adapter import BaseSearchAdapter
from tools.search.schemas import (
    SearchProvider,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


class SerpAPIAdapter(BaseSearchAdapter):

    BASE_URL = "https://serpapi.com/search"

    def __init__(self):

        self.client = HTTPClient()

        self.auth = APIKeyAuth(
            api_key=os.getenv("SERPAPI_API_KEY", ""),
            header_name="Authorization",
            prefix="Bearer",
        )

    @property
    def provider_name(self) -> str:
        return SearchProvider.SERPAPI.value

    async def initialize(self):

        if not self.auth.api_key:
            raise RuntimeError(
                "SERPAPI_API_KEY is not configured."
            )

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        response = await self.client.get(

            self.BASE_URL,

            params={
                "q": request.query,
                "num": request.max_results,
                "api_key": self.auth.api_key,
            }

        )

        data = response.json()

        results = []

        for item in data.get("organic_results", []):

            results.append(

                SearchResult(

                    title=item.get("title", ""),

                    url=item.get("link", ""),

                    snippet=item.get("snippet", ""),

                )

            )

        return SearchResponse(

            provider=SearchProvider.SERPAPI,

            total_results=len(results),

            results=results,

        )

    async def close(self):

        await self.client.close()