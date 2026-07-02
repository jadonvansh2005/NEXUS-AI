"""
Memory Stage

Responsibilities

- Invoke Memory Gateway
- Retrieve required memory context
- Update AgentState with retrieved memory

Notes

- Contains NO memory retrieval logic.
- Delegates everything to Memory Gateway.
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


class MemoryStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for memory retrieval.
    """

    stage_name = (

        "memory"

    )

    required_services = [

        "memory_gateway",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        memory_gateway = (

            context.resolve(

                "memory_gateway"

            )

        )

        agent_state: AgentState = (

            memory_gateway.execute(

                state.agent_state,

                db=context.database,

            )

        )

        state.agent_state = (

            agent_state

        )

        return (

            state

        )