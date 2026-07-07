"""
UPSS Browser - Playwright Adapter

Production Playwright Adapter.

Responsibilities
----------------
- Browser navigation
- Page reading
- Screenshots
- Downloads

Browser lifecycle is managed by BrowserSession.
HTML parsing is delegated to HTMLParser and MarkdownParser.
"""

from __future__ import annotations

from pathlib import Path

from playwright.async_api import Page

from tools.browser.browser_session import BrowserSession
from tools.browser.adapters.base_browser_adapter import BaseBrowserAdapter
from tools.browser.parsers.html_parser import HTMLParser
from tools.browser.parsers.markdown_parser import MarkdownParser
from tools.browser.schemas import (
    BrowserPage,
    BrowserRequest,
    BrowserResponse,
)


class PlaywrightAdapter(BaseBrowserAdapter):
    """
    Production Playwright Adapter.

    Browser lifecycle is handled by BrowserSession.
    """

    def __init__(self):

        self.session: BrowserSession | None = None

    async def initialize(self):

        if self.session is None:
            self.session = await BrowserSession.get_instance()

    async def _get_page(
        self,
        page_name: str = "default",
    ) -> Page:

        if self.session is None:
            await self.initialize()

        return await self.session.get_page(page_name)

    async def read(
        self,
        request: BrowserRequest,
    ) -> BrowserResponse:

        page = await self._get_page("reader")

        await page.goto(
            request.url,
            wait_until=request.wait_until,
            timeout=request.timeout * 1000,
        )

        html = await page.content()

        title = HTMLParser.extract_title(html)

        text = HTMLParser.extract_text(html)

        markdown = MarkdownParser.to_markdown(
            html
        )

        # Log to history
        try:
            from tools.register_tools import registry
            history_tool = registry.get_tool("browser.history")
            if history_tool:
                history_tool.add_entry(request.url, title or "Webpage")
        except Exception as e:
            print(f"[History Logger Error] {e}")

        return BrowserResponse(
            success=True,
            page=BrowserPage(
                url=request.url,
                title=title,
                html=html,
                text=text,
                markdown=markdown,
            ),
            message="Page loaded successfully.",
        )

    async def screenshot(
        self,
        request: BrowserRequest,
    ) -> str:

        page = await self._get_page("screenshot")

        await page.goto(
            request.url,
            wait_until=request.wait_until,
            timeout=request.timeout * 1000,
        )

        # Log to history
        try:
            title = await page.title()
            from tools.register_tools import registry
            history_tool = registry.get_tool("browser.history")
            if history_tool:
                history_tool.add_entry(request.url, title or "Screenshot Capture")
        except Exception as e:
            print(f"[History Logger Error] {e}")

        import time
        from urllib.parse import urlparse
        
        parsed_url = urlparse(request.url)
        domain = parsed_url.netloc.replace(":", "_").replace(".", "_")
        filename = f"screenshot_{domain}_{int(time.time())}.png"
        
        download_dir = Path("downloads")
        download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        
        file_path = download_dir / filename
        await page.screenshot(
            path=str(file_path),
            full_page=True,
            type="png",
        )

        return str(file_path)

    async def download(
        self,
        request: BrowserRequest,
    ) -> str:

        page = await self._get_page("download")

        async with page.expect_download() as download_info:

            await page.goto(
                request.url,
                wait_until=request.wait_until,
                timeout=request.timeout * 1000,
            )

        download = await download_info.value

        download_dir = Path("downloads")

        download_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = download_dir / download.suggested_filename

        await download.save_as(file_path)

        return str(file_path)

    async def close(self):
        """
        BrowserSession owns the browser lifecycle.

        Nothing to close here.
        """
        return