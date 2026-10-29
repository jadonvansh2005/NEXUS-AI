
from __future__ import annotations

import re


class ToolRouter:
    """
    Routes only clearly identifiable filesystem requests to MCP.
    All other requests remain with the existing UPSS pipeline.
    """

    _READ_PATTERNS = (
        r"\b(list|show|display)\s+(all\s+)?(the\s+)?files\b",
        r"\b(list|show|display)\s+(the\s+)?(contents\s+of\s+)?"
        r"(the\s+)?(directory|folder)\b",
        r"\b(read|open|display|show)\s+(the\s+)?file\b",
        r"\b(search|find|locate)\s+(for\s+)?"
        r"(the\s+)?(file|filename|files)\b",
        r"\bsearch\s+for\s+['\"].+['\"]",
    )

    _WRITE_PATTERNS = (
        r"\b(create|make|write|edit|modify|move|rename|delete|remove)\s+"
        r"(the\s+)?(file|folder|directory)\b",
    )

    def route(self, query: str) -> str:
        """
        Returns 'filesystem_mcp' only for recognized filesystem requests;
        otherwise returns 'upss'.
        """
        if not isinstance(query, str) or not query.strip():
            return "upss"

        normalized = query.strip().lower()

        # Keep writes out of the initial read-only integration.
        if any(
            re.search(pattern, normalized)
            for pattern in self._WRITE_PATTERNS
        ):
            return "upss"

        if any(
            re.search(pattern, normalized)
            for pattern in self._READ_PATTERNS
        ):
            return "filesystem_mcp"

        return "upss"
