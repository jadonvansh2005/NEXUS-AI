"""
Pipeline Manager

Responsibilities

- Initialize runtime pipeline
- Build execution pipeline
- Execute pipeline
- Return final pipeline state

Notes

- Public entry point of the Integration Layer.
- Coordinates Builder and Executor.
- Does NOT contain business logic.
"""

from __future__ import annotations

from integration.pipeline_builder import (
    PipelineBuilder,
)

from integration.pipeline_context import (
    PipelineContext,
)

from integration.pipeline_executor import (
    PipelineExecutor,
)

from integration.pipeline_state import (
    PipelineState,
)

from integration.stage_registry import (
    StageRegistry,
)

from agents.core.agent_state import (
    AgentState,
)


class PipelineManager:

    """
    Main runtime manager for UPSS.
    """

    def __init__(

        self,

        registry: StageRegistry,

        context: PipelineContext,

    ):

        self.registry = registry

        self.context = context

        self.builder = (

            PipelineBuilder(

                registry

            )

        )

        self.executor = (

            PipelineExecutor()

        )

    # =====================================================
    # Execute Pipeline
    # =====================================================

    def execute(

        self,

        agent_state: AgentState,

    ) -> PipelineState:

        #
        # Create Runtime State
        #

        pipeline_state = (

            PipelineState(

                agent_state=agent_state

            )

        )

        #
        # Build Runtime Pipeline
        #

        pipeline = (

            self.builder.build(

                pipeline_state

            )

        )

        #
        # Execute
        #

        pipeline_state = (

            self.executor.execute(

                pipeline=pipeline,

                state=pipeline_state,

                context=self.context,

            )

        )

        return (

            pipeline_state

        )