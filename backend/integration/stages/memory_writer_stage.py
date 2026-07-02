"""
Memory Writer Stage

Responsibilities

- Persist conversation memory
- Persist user facts
- Persist long-term memory
- Update AgentState

Notes

- Contains NO memory writing logic.
- Delegates everything to Memory Writer.
"""

from __future__ import annotations

from integration.pipeline_context import (
    PipelineContext,
)

from integration.pipeline_state import (
    PipelineState,
)

from integration.stages.base_stage import (
    BaseStage,
)

from agents.core.agent_state import (
    AgentState,
)


class MemoryWriterStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for persisting memories.
    """

    stage_name = (

        "memory_writer"

    )

    required_services = [

        "memory_writer",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        memory_writer = (

            context.resolve(

                "memory_writer"

            )

        )

        #
        # Persist memories.
        #

        agent_state: AgentState = (

            memory_writer.execute(

                state.agent_state

            )

        )

        #
        # Update Pipeline State
        #

        state.agent_state = (

            agent_state

        )

        return (

            state

        )