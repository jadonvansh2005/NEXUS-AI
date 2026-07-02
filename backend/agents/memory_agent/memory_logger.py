"""
Memory Logger

Responsibilities

- Log memory retrieval
- Log memory writes
- Log routing
- Log validation
- Log failures

Future

- LangSmith
- OpenTelemetry
- ELK
- Grafana
"""

from __future__ import annotations

import logging

from agents.memory_agent.memory_state import (
    MemoryState,
)


logger = logging.getLogger(__name__)


class MemoryLogger:

    """
    Centralized logger for Memory Agent.
    """

    # =====================================================
    # Memory Request
    # =====================================================

    def retrieval_started(

        self,

        state: MemoryState,

    ) -> None:

        logger.info(

            "[Memory] Retrieval Started | "

            "User=%s | Query=%s",

            state.user_id,

            state.query,

        )

    # =====================================================
    # Routing
    # =====================================================

    def routing_completed(

        self,

        state: MemoryState,

    ) -> None:

        logger.info(

            "[Memory] Routes -> %s",

            [

                memory.value

                for memory

                in state.requested_memory_types

            ],

        )

    # =====================================================
    # Retrieval Completed
    # =====================================================

    def retrieval_completed(

        self,

        state: MemoryState,

    ) -> None:

        logger.info(

            "[Memory] Retrieved | "

            "Facts=%d | "

            "Episodes=%d | "

            "Semantic=%d | "

            "Knowledge=%d | "

            "ShortTerm=%d | "

            "LongTerm=%d",

            len(state.retrieved_facts),

            len(state.retrieved_episodes),

            len(state.retrieved_semantic),

            len(state.retrieved_knowledge),

            len(state.retrieved_short_term),

            len(state.retrieved_long_term),

        )

    # =====================================================
    # Memory Write
    # =====================================================

    def memory_written(

        self,

        memory_type: str,

    ) -> None:

        logger.info(

            "[Memory] Stored -> %s",

            memory_type,

        )

    # =====================================================
    # Validation Failed
    # =====================================================

    def validation_failed(

        self,

    ) -> None:

        logger.error(

            "[Memory] Validation Failed"

        )

    # =====================================================
    # Retrieval Failed
    # =====================================================

    def retrieval_failed(

        self,

        error: str,

    ) -> None:

        logger.error(

            "[Memory] Retrieval Failed | %s",

            error,

        )