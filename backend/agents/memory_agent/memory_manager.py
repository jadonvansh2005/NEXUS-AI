"""
Memory Manager

Responsibilities

- Coordinate memory retrieval
- Validate memory request
- Route memory request
- Execute retrieval
- Build final memory context

Future

- Memory Writing
- Memory Compression
- Reflection Integration
- Cache Layer
"""

from __future__ import annotations

from agents.memory_agent.memory_logger import (
    MemoryLogger,
)

from agents.memory_router.memory_router import (
    MemoryRouter,
)

from agents.memory_agent.memory_state import (
    MemoryState,
)

from agents.memory_agent.memory_validator import (
    MemoryValidator,
)

from agents.memory_agent.retrieval_executor import (
    RetrievalExecutor,
)

from agents.memory_agent.response_manager import (
    ResponseManager,
)


class MemoryManager:

    """
    Coordinates the complete memory pipeline.
    """

    def __init__(self):

        self.validator = (
            MemoryValidator()
        )

        self.router = (
            MemoryRouter()
        )

        self.executor = (
            RetrievalExecutor()
        )

        self.response_manager = (
            ResponseManager()
        )

        self.logger = (
            MemoryLogger()
        )

    # =====================================================
    # Retrieve Context
    # =====================================================

    def retrieve_context(

        self,

        db,

        state: MemoryState,

    ):

        #
        # Decide memory sources
        #

        self.router.route(

            state

        )

        #
        # Validate
        #

        if not self.validator.validate(

            state

        ):

            self.logger.validation_failed()

            return []

        #
        # Logging
        #

        self.logger.retrieval_started(

            state

        )

        self.logger.routing_completed(

            state

        )

        #
        # Execute retrieval
        #

        self.executor.execute(

            db=db,

            state=state,

        )

        self.logger.retrieval_completed(

            state

        )

        #
        # Merge retrieved memories
        #

        return self.response_manager.build_context(

            state

        )