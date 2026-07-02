"""
Pipeline Executor

Responsibilities

- Execute pipeline stages
- Validate stage dependencies
- Maintain execution lifecycle
- Propagate PipelineState

Notes

- Does NOT know business logic.
- Executes stages through BaseStage interface.
"""

from __future__ import annotations

from typing import List

from integration.pipeline_context import (
    PipelineContext,
)

from integration.pipeline_state import (
    PipelineState,
)

from integration.stages.base_stage import (
    BaseStage,
)


class PipelineExecutor:

    """
    Executes an ordered pipeline.
    """

    # =====================================================
    # Execute Pipeline
    # =====================================================

    def execute(

        self,

        pipeline: List[BaseStage],

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        for stage in pipeline:

            #
            # Validate Dependencies
            #

            stage.validate_services(

                context

            )

            try:

                #
                # Before
                #

                stage.before_execute(

                    state

                )

                #
                # Execute
                #

                state = stage.execute(

                    state,

                    context,

                )

                #
                # After
                #

                stage.after_execute(

                    state

                )

            except Exception as exception:

                #
                # Error
                #

                stage.on_error(

                    state,

                    exception,

                )

        #
        # Pipeline Finished
        #

        state.set_completed()

        return state