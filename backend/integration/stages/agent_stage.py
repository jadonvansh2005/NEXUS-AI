"""
Agent Team Stage

Responsibilities

- Build agent collaboration team
- Select participating agents
- Update AgentState

Notes

- Contains NO agent selection logic.
- Delegates everything to the Collaboration module.
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


class AgentStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for building the collaborating
    agent team.
    """

    stage_name = (

        "agent_team"

    )

    required_services = [

        "collaboration",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        collaboration = (

            context.resolve(

                "collaboration"

            )

        )

        agent_state: AgentState = (

            collaboration.execute(

                state.agent_state

            )

        )

        state.agent_state = (

            agent_state

        )

        return (

            state

        )