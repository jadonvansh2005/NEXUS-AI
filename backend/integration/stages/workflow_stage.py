"""
Workflow Stage

Responsibilities

- Invoke Workflow Engine
- Transform execution plan into executable workflow
- Update AgentState

Notes

- Contains NO workflow logic.
- Delegates workflow generation to Workflow Engine.
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


class WorkflowStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for workflow generation.
    """

    stage_name = (

        "workflow"

    )

    required_services = [

        "workflow",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        workflow_engine = (

            context.resolve(

                "workflow"

            )

        )

        agent_state: AgentState = (

            workflow_engine.execute(

                state.agent_state

            )

        )

        state.agent_state = (

            agent_state

        )

        return (

            state

        )