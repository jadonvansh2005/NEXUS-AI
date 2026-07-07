"""
Workflow State

Responsibilities

- Store runtime workflow state
- Track task execution
- Track retries
- Track current task

Future

- Checkpointing
- Recovery
- Pause / Resume
"""

from __future__ import annotations

from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from agents.workflow.workflow_models import (
    WorkflowStatus,
    WorkflowTaskStatus,
)


# ==========================================================
# Runtime Task State
# ==========================================================

class RuntimeTaskState(BaseModel):
    """
    Runtime information for a single task.
    """

    task_id: str

    status: WorkflowTaskStatus = (
        WorkflowTaskStatus.PENDING
    )

    retry_count: int = 0

    error: Optional[str] = None


# ==========================================================
# Workflow Runtime State
# ==========================================================

class WorkflowState(BaseModel):
    """
    Runtime workflow state.
    """

    workflow_status: WorkflowStatus = (
        WorkflowStatus.CREATED
    )

    current_task: Optional[str] = None

    completed_tasks: int = 0

    failed_tasks: int = 0

    runtime_tasks: Dict[
        str,
        RuntimeTaskState
    ] = Field(
        default_factory=dict
    )

    metadata: Dict = Field(
        default_factory=dict
    )

    results: Dict = Field(
        default_factory=dict
    )

    file_path: str = ""

    # ======================================================
    # Helpers
    # ======================================================

    def add_task(
        self,
        task_id: str,
    ) -> None:

        self.runtime_tasks[
            task_id
        ] = RuntimeTaskState(
            task_id=task_id
        )

    def update_status(
        self,
        task_id: str,
        status: WorkflowTaskStatus,
    ) -> None:

        if task_id not in self.runtime_tasks:

            return

        self.runtime_tasks[
            task_id
        ].status = status

    def increment_retry(
        self,
        task_id: str,
    ) -> None:

        if task_id not in self.runtime_tasks:

            return

        self.runtime_tasks[
            task_id
        ].retry_count += 1

    def mark_error(
        self,
        task_id: str,
        error: str,
    ) -> None:

        if task_id not in self.runtime_tasks:

            return

        self.runtime_tasks[
            task_id
        ].error = error