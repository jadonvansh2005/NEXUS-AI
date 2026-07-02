"""
UPSS Browser Session

Production-ready browser session manager.

Responsibilities
----------------
- Singleton browser instance
- Persistent browser context
- Named page management
- Session reuse
- Graceful shutdown
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


class BrowserSession:

    _instance: "BrowserSession | None" = None
    _lock = asyncio.Lock()

    def __init__(self):

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None

        self._pages: dict[str, Page] = {}

        self._initialized = False

    # ======================================================
    # Singleton
    # ======================================================

    @classmethod
    async def get_instance(cls) -> "BrowserSession":

        async with cls._lock:

            if cls._instance is None:

                cls._instance = cls()

                await cls._instance.initialize()

            return cls._instance

    # ======================================================
    # Initialization
    # ======================================================

    async def initialize(self):

        if self._initialized:
            return

        self._playwright = await async_playwright().start()

        self._browser = await self._playwright.chromium.launch(
            headless=True,
        )

        self._context = await self._browser.new_context(
            accept_downloads=True,
            viewport={
                "width": 1440,
                "height": 900,
            },
        )

        self._initialized = True

    # ======================================================
    # Page Management
    # ======================================================

    async def get_page(
        self,
        name: str = "default",
    ) -> Page:

        if name in self._pages:

            page = self._pages[name]

            if not page.is_closed():

                return page

        page = await self._context.new_page()

        self._pages[name] = page

        return page

    async def close_page(
        self,
        name: str,
    ):

        page = self._pages.get(name)

        if page:

            if not page.is_closed():

                await page.close()

            self._pages.pop(name, None)

    async def close_all_pages(self):

        for page in list(self._pages.values()):

            if not page.is_closed():

                await page.close()

        self._pages.clear()

    # ======================================================
    # Cookies
    # ======================================================

    async def save_storage(
        self,
        path: str = "browser_storage.json",
    ):

        await self._context.storage_state(
            path=path
        )

    async def load_storage(
        self,
        path: str = "browser_storage.json",
    ):

        if not Path(path).exists():
            return

        if self._browser:

            await self._context.close()

            self._context = await self._browser.new_context(
                storage_state=path,
                accept_downloads=True,
            )

    # ======================================================
    # Shutdown
    # ======================================================

    async def shutdown(self):

        await self.close_all_pages()

        if self._context:

            await self._context.close()

            self._context = None

        if self._browser:

            await self._browser.close()

            self._browser = None

        if self._playwright:

            await self._playwright.stop()

            self._playwright = None

        self._initialized = False