"""
Stage Registry

Responsibilities

- Register pipeline stages
- Resolve stages
- Maintain execution order
- Build executable pipeline

Notes

- Does NOT execute stages.
- Does NOT contain business logic.
- Only manages stage registration.
"""

from __future__ import annotations

from collections import OrderedDict

from typing import Dict
from typing import List
from typing import Optional

from integration.stages.base_stage import (
    BaseStage,
)


class StageRegistry:

    """
    Registry for all pipeline stages.
    """

    def __init__(

        self,

    ):

        #
        # Ordered Stage Registry
        #

        self._stages: Dict[

            str,

            BaseStage

        ] = OrderedDict()

    # =====================================================
    # Register
    # =====================================================

    def register(

        self,

        stage: BaseStage,

    ) -> None:

        self._stages[

            stage.stage_name

        ] = stage

    # =====================================================
    # Unregister
    # =====================================================

    def unregister(

        self,

        stage_name: str,

    ) -> None:

        self._stages.pop(

            stage_name,

            None,

        )

    # =====================================================
    # Resolve
    # =====================================================

    def resolve(

        self,

        stage_name: str,

    ) -> Optional[BaseStage]:

        return self._stages.get(

            stage_name

        )

    # =====================================================
    # Exists
    # =====================================================

    def contains(

        self,

        stage_name: str,

    ) -> bool:

        return (

            stage_name

            in

            self._stages

        )

    # =====================================================
    # List Stages
    # =====================================================

    def list_stages(

        self,

    ) -> List[str]:

        return list(

            self._stages.keys()

        )

    # =====================================================
    # Ordered Pipeline
    # =====================================================

    def build_pipeline(

        self,

        stage_names: List[str],

    ) -> List[BaseStage]:

        pipeline: List[BaseStage] = []

        for stage_name in stage_names:

            stage = self.resolve(

                stage_name

            )

            if stage is None:

                raise RuntimeError(

                    f"Pipeline stage "

                    f"'{stage_name}' "

                    f"is not registered."

                )

            pipeline.append(

                stage

            )

        return pipeline

    # =====================================================
    # All Stages
    # =====================================================

    def all(

        self,

    ) -> List[BaseStage]:

        return list(

            self._stages.values()

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(

        self,

    ) -> None:

        self._stages.clear()

    # =====================================================
    # Count
    # =====================================================

    def count(

        self,

    ) -> int:

        return len(

            self._stages

        )