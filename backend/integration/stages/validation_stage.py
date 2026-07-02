"""
Validation Stage

Responsibilities

- Validate execution results
- Verify workflow output
- Detect execution failures
- Update AgentState

Notes

- Contains NO validation logic.
- Delegates everything to Validation Manager.
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


class ValidationStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for validating execution results.
    """

    stage_name = (

        "validation"

    )

    required_services = [

        "validator",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        validator = (

            context.resolve(

                "validator"

            )

        )

        #
        # Validate execution results.
        #

        agent_state: AgentState = (

            validator.execute(

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