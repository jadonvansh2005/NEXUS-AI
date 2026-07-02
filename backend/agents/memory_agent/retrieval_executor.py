"""
Retrieval Executor

Responsibilities

- Execute memory retrieval
- Call appropriate memory services
- Populate MemoryState

Future

- Parallel Retrieval
- Async Retrieval
- Hybrid Retrieval
- Reflection Feedback
"""

from __future__ import annotations

from agents.memory_agent.memory_models import (
    MemoryType,
)

from agents.memory_agent.memory_state import (
    MemoryState,
)

from memory.fact_memory.fact_service import (
    FactService,
)

from memory.recall.recall_service import (
    RecallService,
)


class RetrievalExecutor:

    """
    Executes retrieval from the requested
    memory sources.
    """

    def __init__(self):

        self.fact_service = (
            FactService()
        )

        self.recall_service = (
            RecallService()
        )

    # =====================================================
    # Execute Retrieval
    # =====================================================

    def execute(

        self,

        db,

        state: MemoryState,

    ) -> None:

        for memory_type in state.requested_memory_types:

            #
            # ----------------------------------------------
            # Fact Memory
            # ----------------------------------------------
            #

            if memory_type == MemoryType.FACT:

                facts = (

                    self.fact_service.get_user_facts(

                        db=db,

                        user_id=state.user_id,

                    )

                )

                if facts:

                    state.retrieved_facts.extend(

                        facts

                    )

            #
            # ----------------------------------------------
            # Episodic / Recall Memory
            # ----------------------------------------------
            #

            elif memory_type == MemoryType.EPISODIC:

                messages = (

                    self.recall_service.get_user_messages(

                        db=db,

                        user_id=state.user_id,

                    )

                )

                if messages:

                    state.retrieved_episodes.extend(

                        messages

                    )

            #
            # ----------------------------------------------
            # Semantic Memory
            # ----------------------------------------------
            #

            elif memory_type == MemoryType.SEMANTIC:

                #
                # Future:
                # Semantic Memory Service
                #

                pass

            #
            # ----------------------------------------------
            # Knowledge Memory (RAG)
            # ----------------------------------------------
            #

            elif memory_type == MemoryType.KNOWLEDGE:

                #
                # Future:
                # RAG Retrieval
                #

                pass

            #
            # ----------------------------------------------
            # Short-Term Memory
            # ----------------------------------------------
            #

            elif memory_type == MemoryType.SHORT_TERM:

                #
                # Future:
                # Conversation Buffer
                #

                pass

            #
            # ----------------------------------------------
            # Long-Term Memory
            # ----------------------------------------------
            #

            elif memory_type == MemoryType.LONG_TERM:

                #
                # Future:
                # Long-Term Store
                #

                pass