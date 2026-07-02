"""
Execution State

Responsibilities

- Store execution runtime
- Track current execution
- Store execution result
- Store execution errors

Future

- Distributed Workers
- Checkpointing
- Streaming Results
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from agents.execution.execution_models import (
    ExecutionStatus,
)


# ==========================================================
# Execution State
# ==========================================================

class ExecutionState(BaseModel):
    """
    Runtime state of a tool execution.
    """

    #
    # Current Task
    #

    task_id: Optional[str] = None

    tool_name: Optional[str] = None

    provider_name: Optional[str] = None

    execution_result: Any | None = None

    #
    # Execution Status
    #

    status: ExecutionStatus = (
        ExecutionStatus.CREATED
    )

    #
    # Retry Information
    #

    retry_count: int = 0

    #
    # Execution Output
    #

    result: Optional[Any] = None

    error: Optional[str] = None

    #
    # Metrics
    #

    execution_time_ms: float = 0.0

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    # =====================================================
    # Helpers
    # =====================================================

    def start(
        self,
    ) -> None:

        self.status = (
            ExecutionStatus.RUNNING
        )

    def complete(
        self,
        result: Any,
    ) -> None:

        self.status = (
            ExecutionStatus.COMPLETED
        )

        self.result = result

    def fail(
        self,
        error: str,
    ) -> None:

        self.status = (
            ExecutionStatus.FAILED
        )

        self.error = error

    def retry(
        self,
    ) -> None:

        self.retry_count += 1

        self.status = (
            ExecutionStatus.RETRYING
        )

    def cancel(
        self,
    ) -> None:

        self.status = (
            ExecutionStatus.CANCELLED
        )