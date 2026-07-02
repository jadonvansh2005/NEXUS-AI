"""
Planner Memory

Responsibilities

- Prepare memory for the Planner.
- Filter relevant memories.
- Build planning context.

Future

- Semantic Memory
- Episodic Memory
- Preference Memory
- Working Memory
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List


class PlannerMemory:

    """
    Planner memory helper.
    """

    def build_context(

        self,

        memories: List[Dict[str, Any]],

    ) -> List[Dict[str, Any]]:

        #
        # Future
        #
        # Rank memories
        # Remove duplicates
        # Summarize long memories
        # Semantic filtering
        #

        return memories

    def extract_preferences(

        self,

        memories: List[Dict[str, Any]],

    ) -> Dict[str, Any]:

        preferences: Dict[str, Any] = {}

        for memory in memories:

            key = memory.get("fact_key")

            value = memory.get("fact_value")

            if key and value:

                preferences[key] = value

        return preferences

    def recent_context(

        self,

        conversations: List[Dict[str, Any]],

    ) -> List[Dict[str, Any]]:

        #
        # Future
        #
        # Last N messages
        # Conversation summarization
        #

        return conversations