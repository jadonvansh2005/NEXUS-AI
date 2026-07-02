"""
UPSS Browser Adapter
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from tools.browser.schemas import (
    BrowserRequest,
    BrowserResponse,
)


class BaseBrowserAdapter(ABC):

    @abstractmethod
    async def initialize(self):
        ...

    @abstractmethod
    async def read(
        self,
        request: BrowserRequest,
    ) -> BrowserResponse:
        ...

    @abstractmethod
    async def screenshot(
        self,
        request: BrowserRequest,
    ) -> bytes:
        ...

    @abstractmethod
    async def download(
        self,
        request: BrowserRequest,
    ) -> str:
        ...

    @abstractmethod
    async def close(self):
        ...