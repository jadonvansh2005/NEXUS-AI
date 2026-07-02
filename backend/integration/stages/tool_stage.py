"""
Tool Stage

Responsibilities

- Select required tools
- Prepare execution resources
- Update AgentState

Notes

- Contains NO tool execution logic.
- Delegates tool selection to Tool Selector.
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


class ToolStage(

    BaseStage

):

    """
    Pipeline stage responsible
    for preparing tools required
    for execution.
    """

    stage_name = (

        "tool"

    )

    required_services = [

        "tool_selector",

    ]

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        tool_selector = (

            context.resolve(

                "tool_selector"

            )

        )

        #
        # Tool Selector decides
        # which tools are required.
        #

        agent_state: AgentState = (

            tool_selector.execute(

                state.agent_state

            )

        )

        state.agent_state = (

            agent_state

        )

        return (

            state

        )