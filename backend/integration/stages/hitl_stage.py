"""
HITL Stage

Responsibilities

- Handle Human-in-the-Loop decisions
- Request approval when required
- Update AgentState

Notes

- Contains NO HITL logic.
- Delegates everything to HITL Agent.
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


class HITLStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for Human-in-the-Loop.
    """

    stage_name = (

        "hitl"

    )

    required_services = [

        "hitl",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        hitl = (

            context.resolve(

                "hitl"

            )

        )

        #
        # Execute Human-in-the-Loop.
        #

        agent_state: AgentState = (

            hitl.execute(

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