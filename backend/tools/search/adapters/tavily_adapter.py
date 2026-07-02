"""
UPSS Search - Tavily Adapter

Implements BaseSearchAdapter using Tavily Search API.
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


class TavilyAdapter(BaseSearchAdapter):

    BASE_URL = "https://api.tavily.com/search"

    def __init__(self):

        self.client = HTTPClient()

        self.auth = APIKeyAuth(
            api_key=os.getenv("TAVILY_API_KEY", ""),
            header_name="Authorization",
            prefix="Bearer",
        )

    @property
    def provider_name(self) -> str:

        return SearchProvider.TAVILY.value

    async def initialize(self):

        if not self.auth.api_key:
            raise RuntimeError(
                "TAVILY_API_KEY is not configured."
            )

    async def search(
        self,
        request: SearchRequest,
    ) -> SearchResponse:

        payload = {

            "query": request.query,

            "max_results": request.max_results,

            "search_depth": "advanced",

            "include_answer": False,

            "include_images": False,
        }

        response = await self.client.post(

            self.BASE_URL,

            headers=self.auth.headers(),

            json=payload,

        )

        data = response.json()

        results = []

        for item in data.get("results", []):

            results.append(

                SearchResult(

                    title=item.get("title", ""),

                    url=item.get("url", ""),

                    snippet=item.get("content", ""),

                )

            )

        return SearchResponse(

            provider=SearchProvider.TAVILY,

            total_results=len(results),

            results=results,

        )

    async def close(self):

        await self.client.close()