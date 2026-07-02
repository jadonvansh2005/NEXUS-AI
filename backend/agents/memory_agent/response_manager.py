"""
Response Manager

Responsibilities

- Build final memory context
- Merge retrieved memories
- Remove duplicates
- Prepare LLM context

Future

- Context Compression
- Token Budgeting
- LLM Prompt Formatting
- Memory Ranking
"""

from __future__ import annotations

from typing import List

from agents.memory_agent.memory_state import (
    MemoryState,
)


class ResponseManager:

    """
    Builds the final memory context
    returned by the Memory Agent.
    """

    # =====================================================
    # Build Context
    # =====================================================

    def build_context(

        self,

        state: MemoryState,

    ) -> List[str]:

        context: List[str] = []

        #
        # ----------------------------------------------
        # Facts
        # ----------------------------------------------
        #

        for fact in state.retrieved_facts:

            value = getattr(

                fact,

                "fact_value",

                str(fact),

            )

            context.append(

                str(value)

            )

        #
        # ----------------------------------------------
        # Episodic Memory
        # ----------------------------------------------
        #

        for message in state.retrieved_episodes:

            value = getattr(

                message,

                "content",

                str(message),

            )

            context.append(

                str(value)

            )

        #
        # ----------------------------------------------
        # Semantic Memory
        # ----------------------------------------------
        #

        for memory in state.retrieved_semantic:

            context.append(

                str(memory)

            )

        #
        # ----------------------------------------------
        # Knowledge Memory
        # ----------------------------------------------
        #

        for memory in state.retrieved_knowledge:

            context.append(

                str(memory)

            )

        #
        # ----------------------------------------------
        # Short-Term Memory
        # ----------------------------------------------
        #

        for memory in state.retrieved_short_term:

            context.append(

                str(memory)

            )

        #
        # ----------------------------------------------
        # Long-Term Memory
        # ----------------------------------------------
        #

        for memory in state.retrieved_long_term:

            context.append(

                str(memory)

            )

        #
        # Remove duplicates
        #

        unique_context = list(

            dict.fromkeys(

                context

            )

        )

        #
        # Save into state
        #

        state.context = unique_context

        return unique_context