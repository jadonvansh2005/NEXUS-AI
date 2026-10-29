
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from integration.mcp_client import CombinedMCPClient, BACKEND_ROOT


class FilesystemMCPHandler:
    """
    Independent, read-only natural-language handler for Filesystem MCP.

    Does not register tools in the existing UPSS ToolRegistry.
    """

    def __init__(self, client: CombinedMCPClient):
        self.client = client

    @staticmethod
    def _extract_path(query: str) -> str | None:
        """Extract a quoted path, or a Windows/POSIX path from the query."""
        quoted = re.search(r"""["']([^"']+)["']""", query)

        if quoted:
            return quoted.group(1).strip()

        path_match = re.search(
            r"""(?:[A-Za-z]:\\[^\s"'<>|?*]+|/[^\s"'<>|?*]+)""",
            query,
        )

        if path_match:
            return path_match.group(0).rstrip(".,;:")

        return None

    @staticmethod
    def _format_result(result: Any) -> str:
        """Convert an MCP result into readable text."""
        if getattr(result, "isError", False):
            raise RuntimeError("The Filesystem MCP tool reported an error.")

        content = getattr(result, "content", None)

        if content:
            parts = [
                item.text
                for item in content
                if getattr(item, "text", None) is not None
            ]
            if parts:
                return "\n".join(parts)

        return str(result)

    async def handle_query(self, query: str) -> dict:
        """
        Handle a basic filesystem request.

        Returns a structured result instead of modifying chatbot responses.
        """
        if not isinstance(query, str) or not query.strip():
            return {
                "success": False,
                "message": "Please provide a filesystem request.",
            }

        text = query.strip()
        lower = text.lower()
        path = self._extract_path(text)

        # Write operations are deliberately not executed in this first version.
        write_words = (
            "create file",
            "make file",
            "write file",
            "edit file",
            "modify file",
            "move file",
            "rename file",
            "delete file",
            "remove file",
        )

        if any(word in lower for word in write_words):
            return {
                "success": False,
                "requires_confirmation_flow": True,
                "message": (
                    "This operation is not enabled in the initial read-only "
                    "Filesystem MCP handler."
                ),
            }

        
        if any(word in lower for word in ("search", "find")):
            quoted = re.search(r"""["']([^"']+)["']""", text)
            quoted_value = quoted.group(1).strip() if quoted else None

            # A quoted absolute path may specify the search root.
            if quoted_value and (
                Path(quoted_value).is_absolute()
                or (len(quoted_value) > 1 and quoted_value[1] == ":")
            ):
                root = quoted_value
                pattern = "*"
            else:
                root = str(BACKEND_ROOT)
                pattern = quoted_value or "*"

            result = await self.client.call_tool(
                "filesystem.search_files",
                {
                    "root": root,
                    "pattern": pattern,
                    "max_results": 100,
                },
            )

            return {
                "success": True,
                "tool": "filesystem.search_files",
                "message": self._format_result(result),
            }


        if any(word in lower for word in ("read file", "open file", "show file", "read the contents")):
            if not path:
                return {
                    "success": False,
                    "message": (
                        "Please specify the file path, preferably in quotes."
                    ),
                }

            result = await self.client.call_tool(
                "filesystem.read_file",
                {"path": path},
            )

            return {
                "success": True,
                "tool": "filesystem.read_file",
                "message": self._format_result(result),
            }

        if any(word in lower for word in ("list", "directory", "folder", "files")):
            directory = path or str(BACKEND_ROOT)

            result = await self.client.call_tool(
                "filesystem.list_directory",
                {"path": directory},
            )

            return {
                "success": True,
                "tool": "filesystem.list_directory",
                "message": self._format_result(result),
            }

        return {
            "success": False,
            "message": (
                "I couldn't identify a supported filesystem operation. "
                "Try asking to list a directory, search filenames, or read a file."
            ),
        }
