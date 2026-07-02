"""
Base Pipeline Stage

Responsibilities

- Define common stage interface
- Validate required services
- Execute pipeline stage
- Provide common stage metadata

Notes

- Every pipeline stage must inherit this class.
- PipelineExecutor executes stages through this interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import ClassVar
from typing import List

from integration.pipeline_context import (
    PipelineContext,
)

from integration.pipeline_state import (
    PipelineState,
)


class BaseStage(

    ABC

):

    """
    Base class for all pipeline stages.
    """

    #
    # Stage Name
    #

    stage_name: ClassVar[str] = "base_stage"

    #
    # Services required by this stage.
    #

    required_services: ClassVar[List[str]] = []

    #
    # --------------------------------------------------
    # Execute
    # --------------------------------------------------
    #

    @abstractmethod
    def execute(

        self,

        state: PipelineState,

        context: PipelineContext,

    ) -> PipelineState:

        """
        Execute the stage.

        Must return updated PipelineState.
        """

        raise NotImplementedError

    #
    # --------------------------------------------------
    # Validate Dependencies
    # --------------------------------------------------
    #

    def validate_services(

        self,

        context: PipelineContext,

    ) -> None:

        missing = [

            service

            for service in self.required_services

            if not context.contains(

                service

            )

        ]

        if missing:

            raise RuntimeError(

                f"{self.stage_name} "

                f"requires missing services: "

                f"{', '.join(missing)}"

            )

    #
    # --------------------------------------------------
    # Before Execute
    # --------------------------------------------------
    #

    def before_execute(

        self,

        state: PipelineState,

    ) -> None:

        state.enter_stage(

            self.stage_name

        )

    #
    # --------------------------------------------------
    # After Execute
    # --------------------------------------------------
    #

    def after_execute(

        self,

        state: PipelineState,

    ) -> None:

        state.complete_stage(

            self.stage_name

        )

    #
    # --------------------------------------------------
    # On Error
    # --------------------------------------------------
    #

    def on_error(

        self,

        state: PipelineState,

        exception: Exception,

    ) -> None:

        state.fail_stage(

            self.stage_name

        )

        raise exception