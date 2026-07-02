"""
UPSS HTML Parser

Responsible for extracting clean content from HTML.
"""

from __future__ import annotations

from bs4 import BeautifulSoup


class HTMLParser:
    """
    Extract structured content from HTML.
    """

    @staticmethod
    def extract_title(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        if soup.title:
            return soup.title.get_text(strip=True)

        return ""

    @staticmethod
    def extract_text(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        # Remove unwanted tags
        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav",
                "aside",
                "svg",
            ]
        ):
            tag.decompose()

        return soup.get_text(
            separator="\n",
            strip=True,
        )

    @staticmethod
    def extract_links(html: str) -> list[str]:

        soup = BeautifulSoup(html, "lxml")

        return [
            a["href"]
            for a in soup.find_all("a", href=True)
        ]

    @staticmethod
    def extract_images(html: str) -> list[str]:

        soup = BeautifulSoup(html, "lxml")

        return [
            img["src"]
            for img in soup.find_all("img", src=True)
        ]