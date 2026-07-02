"""
Response Stage

Responsibilities

- Generate final user response
- Format execution output
- Update AgentState

Notes

- Contains NO response generation logic.
- Delegates everything to Response Generator.
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


class ResponseStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for generating the final response.
    """

    stage_name = (

        "response"

    )

    required_services = [

        "response_generator",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        response_generator = (

            context.resolve(

                "response_generator"

            )

        )

        #
        # Generate final response.
        #

        agent_state: AgentState = (

            response_generator.execute(

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