"""
Planner Stage

Responsibilities

- Invoke Planner module
- Update PipelineState
- Continue pipeline execution

Notes

- Contains NO planning logic.
- Delegates planning to PlannerAgent.
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


class PlannerStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for planning.
    """

    stage_name = (

        "planner"

    )

    required_services = [

        "planner",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        planner = (

            context.resolve(

                "planner"

            )

        )

        agent_state: AgentState = (

            planner.execute(

                state.agent_state

            )

        )

        state.agent_state = (

            agent_state

        )

        return (

            state

        )