"""
Pipeline Builder

Responsibilities

- Build runtime execution pipeline
- Validate stage availability
- Construct executable stage sequence

Notes

- Does NOT execute stages.
- Does NOT contain business logic.
- Uses StageRegistry as the source of truth.
"""

from __future__ import annotations

from typing import List

from integration.pipeline_state import (
    PipelineState,
)

from integration.stage_registry import (
    StageRegistry,
)

from integration.stages.base_stage import (
    BaseStage,
)


class PipelineBuilder:

    """
    Builds executable pipelines.
    """

    def __init__(

        self,

        registry: StageRegistry,

    ):

        self.registry = registry

    # =====================================================
    # Build Pipeline
    # =====================================================

    def build(

        self,

        state: PipelineState,

    ) -> List[BaseStage]:

        #
        # Future:
        #
        # Workflow Engine
        # User Settings
        # Runtime Policies
        #
        # can provide different
        # stage sequences.
        #

        pipeline_definition = (

            state.metadata.get(

                "pipeline_definition"

            )

        )

        #
        # Default Pipeline
        #

        if pipeline_definition is None:

            pipeline_definition = [

                "planner",

                "memory",

                "workflow",

                "agent_team",

                "tool_selection",

                "execution",

            ]

        #
        # Build Runtime Pipeline
        #

        return self.registry.build_pipeline(

            pipeline_definition

        )

    # =====================================================
    # Validate
    # =====================================================

    def validate(

        self,

        stage_names: List[str],

    ) -> bool:

        return all(

            self.registry.contains(

                stage

            )

            for stage

            in stage_names

        )

    # =====================================================
    # Available Stages
    # =====================================================

    def available_stages(

        self,

    ) -> List[str]:

        return self.registry.list_stages()