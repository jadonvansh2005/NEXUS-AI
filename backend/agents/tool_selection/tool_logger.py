"""
Tool Selection Logger

Responsibilities

- Log capability matching
- Log candidate tools
- Log ranking decisions
- Log provider selection
- Log fallback events

Future

- LangSmith
- OpenTelemetry
- ELK Stack
- Prometheus
"""

from __future__ import annotations

import logging

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


logger = logging.getLogger(__name__)


class ToolLogger:

    """
    Centralized logger for Tool Selection Engine.
    """

    # =====================================================
    # Capability
    # =====================================================

    def capability_detected(

        self,

        capabilities: List[str],

    ) -> None:

        logger.info(

            "[Capability] %s",

            capabilities,

        )

    # =====================================================
    # Candidate Tools
    # =====================================================

    def candidate_tools(

        self,

        candidates: List[Dict[str, Any]],

    ) -> None:

        names = []
        for tool in candidates:
            if hasattr(tool, "name"):
                names.append(tool.name)
            elif isinstance(tool, dict) and "name" in tool:
                names.append(tool["name"])
            else:
                names.append(str(tool))

        logger.info(

            "[Candidates] %s",

            names,

        )

    # =====================================================
    # Tool Selection
    # =====================================================

    def tool_selected(

        self,

        tool: Optional[Dict[str, Any]],

    ) -> None:

        if tool is None:

            logger.warning(

                "[Tool] No tool selected"

            )

            return

        name = "unknown"
        if hasattr(tool, "name"):
            name = tool.name
        elif isinstance(tool, dict) and "name" in tool:
            name = tool["name"]

        logger.info(

            "[Tool] Selected -> %s",

            name,

        )

    # =====================================================
    # Provider Selection
    # =====================================================

    def provider_selected(

        self,

        provider: Optional[str],

    ) -> None:

        if provider is None:

            logger.warning(

                "[Provider] No provider selected"

            )

            return

        logger.info(

            "[Provider] Selected -> %s",

            provider,

        )

    # =====================================================
    # Fallback
    # =====================================================

    def fallback_used(

        self,

        tool_name: str,

        replacement: str,

    ) -> None:

        logger.warning(

            "[Fallback] %s -> %s",

            tool_name,

            replacement,

        )

    # =====================================================
    # Selection Failure
    # =====================================================

    def selection_failed(

        self,

        reason: str,

    ) -> None:

        logger.error(

            "[Selection Failed] %s",

            reason,

        )