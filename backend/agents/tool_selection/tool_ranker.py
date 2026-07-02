"""
Tool Ranker

Responsibilities

- Rank candidate tools
- Select best tool
- Score candidates

Future

- LLM Ranking
- Historical Success Rate
- Latency
- Cost
- Provider Health
- User Preferences
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class ToolRanker:

    """
    Select the best tool from candidate tools.
    """

    # =====================================================
    # Public API
    # =====================================================

    def rank(

        self,

        candidates: List[Dict[str, Any]],

    ) -> Optional[Dict[str, Any]]:

        if not candidates:

            return None

        scored_tools = []

        for tool in candidates:

            score = self._score_tool(

                tool

            )

            scored_tools.append(

                (score, tool)

            )

        scored_tools.sort(

            key=lambda item: item[0],

            reverse=True,

        )

        return scored_tools[0][1]

    # =====================================================
    # Tool Scoring
    # =====================================================

    def _score_tool(

        self,

        tool: Dict[str, Any],

    ) -> float:

        score = 0.0

        #
        # Enabled Tool
        #

        if tool.enabled:

            score += 50

        #
        # Provider Availability
        #

        providers = tool.providers

        score += len(

            providers

        ) * 10

        #
        # Capability Count
        #

        capabilities = tool.capabilities

        score += len(

            capabilities

        ) * 2

        return score

    # =====================================================
    # Rank All
    # =====================================================

    def rank_all(

        self,

        candidates: List[Dict[str, Any]],

    ) -> List[Dict[str, Any]]:

        return sorted(

            candidates,

            key=self._score_tool,

            reverse=True,

        )