"""
Pipeline State

Responsibilities

- Runtime pipeline state
- Stage execution tracking
- Pipeline metadata
- Shared execution context

Notes

- Does NOT replace AgentState.
- Wraps AgentState for pipeline execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from agents.core.agent_state import (
    AgentState,
)


@dataclass
class PipelineState:

    # =====================================================
    # Core Runtime
    # =====================================================

    agent_state: AgentState

    # =====================================================
    # Pipeline Runtime
    # =====================================================

    pipeline_id: str = ""

    current_stage: str = ""

    completed_stages: List[str] = field(
        default_factory=list
    )

    failed_stage: Optional[str] = None

    is_completed: bool = False

    # =====================================================
    # Shared Runtime Objects
    # =====================================================

    shared_data: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Diagnostics
    # =====================================================

    execution_trace: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    # =====================================================
    # Helpers
    # =====================================================

    def enter_stage(

        self,

        stage_name: str,

    ) -> None:

        self.current_stage = stage_name

        self.execution_trace.append(

            f"ENTER:{stage_name}"

        )

    def complete_stage(

        self,

        stage_name: str,

    ) -> None:

        self.completed_stages.append(

            stage_name

        )

        self.execution_trace.append(

            f"EXIT:{stage_name}"

        )

    def fail_stage(

        self,

        stage_name: str,

    ) -> None:

        self.failed_stage = stage_name

        self.execution_trace.append(

            f"FAILED:{stage_name}"

        )

    def set_completed(

        self,

    ) -> None:

        self.is_completed = True