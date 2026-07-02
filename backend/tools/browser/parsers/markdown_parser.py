"""
UPSS Markdown Parser

Converts HTML into clean Markdown suitable for LLMs.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup


class MarkdownParser:
    """
    Convert HTML documents into clean Markdown.
    """

    @staticmethod
    def to_markdown(html: str) -> str:

        soup = BeautifulSoup(html, "lxml")

        # --------------------------------------------------
        # Remove unwanted elements
        # --------------------------------------------------

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

        markdown: list[str] = []

        for element in soup.find_all(

            [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "p",
                "pre",
                "code",
                "ul",
                "ol",
                "li",
                "blockquote",
            ]

        ):

            text = element.get_text(
                " ",
                strip=True,
            )

            if not text:
                continue

            # ------------------------------------------

            if element.name == "h1":
                markdown.append(f"# {text}")

            elif element.name == "h2":
                markdown.append(f"## {text}")

            elif element.name == "h3":
                markdown.append(f"### {text}")

            elif element.name == "h4":
                markdown.append(f"#### {text}")

            elif element.name == "h5":
                markdown.append(f"##### {text}")

            elif element.name == "h6":
                markdown.append(f"###### {text}")

            elif element.name == "blockquote":
                markdown.append(f"> {text}")

            elif element.name == "li":
                markdown.append(f"- {text}")

            elif element.name == "code":

                markdown.append(
                    f"`{text}`"
                )

            elif element.name == "pre":

                markdown.append(
                    f"```\n{text}\n```"
                )

            else:

                markdown.append(text)

        content = "\n\n".join(markdown)

        content = re.sub(
            r"\n{3,}",
            "\n\n",
            content,
        )

        return content.strip()