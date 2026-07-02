"""
Schemas for Search Tools
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SearchProvider(str, Enum):

    TAVILY = "tavily"

    SERPAPI = "serpapi"

    BRAVE = "brave"

    DUCKDUCKGO = "duckduckgo"

    AUTO = "auto"


class SearchType(str, Enum):

    WEB = "web"

    IMAGE = "image"

    NEWS = "news"

    ACADEMIC = "academic"

    LOCAL = "local"


class SearchRequest(BaseModel):

    query: str = Field(
        ...,
        description="Search query"
    )

    provider: SearchProvider = SearchProvider.AUTO

    max_results: int = Field(
        default=5,
        ge=1,
        le=20
    )

    language: str = "en"

    safe_search: bool = True


class SearchResult(BaseModel):

    title: str

    url: str

    snippet: str


class SearchResponse(BaseModel):

    provider: SearchProvider

    total_results: int

    results: list[SearchResult]