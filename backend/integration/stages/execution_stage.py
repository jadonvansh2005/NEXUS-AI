"""
Execution Stage

Responsibilities

- Execute workflow
- Delegate execution to Execution Controller
- Update AgentState

Notes

- Contains NO execution logic.
- Delegates execution to Execution Controller.
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


class ExecutionStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for workflow execution.
    """

    stage_name = (

        "execution"

    )

    required_services = [

        "execution_controller",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        execution_controller = (

            context.resolve(

                "execution_controller"

            )

        )

        #
        # Execute the prepared workflow.
        #

        agent_state: AgentState = (

            execution_controller.execute(

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