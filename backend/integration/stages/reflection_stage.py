"""
Reflection Stage

Responsibilities

- Evaluate execution results
- Perform self-reflection
- Improve execution quality
- Update AgentState

Notes

- Contains NO reflection logic.
- Delegates everything to Reflection Agent.
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


class ReflectionStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for reflection and self-correction.
    """

    stage_name = (

        "reflection"

    )

    required_services = [

        "reflection",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        reflection = (

            context.resolve(

                "reflection"

            )

        )

        #
        # Perform reflection.
        #

        agent_state: AgentState = (

            reflection.execute(

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