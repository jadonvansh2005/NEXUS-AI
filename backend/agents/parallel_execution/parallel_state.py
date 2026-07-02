"""
Parallel Execution State

Responsibilities

- Runtime execution state
- Task queues
- Worker information
- Execution results

Future

- Distributed Workers
- Worker Affinity
- Task Priorities
- Dynamic Scaling
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field

from agents.parallel_execution.parallel_models import (
    ExecutionMode,
    ParallelStrategy,
    TaskStatus,
    WorkerInfo,
)


class ParallelState(BaseModel):
    """
    Runtime state for Parallel Execution.
    """

    # =====================================================
    # Workflow
    # =====================================================

    workflow_id: str = ""

    execution_mode: ExecutionMode = (

        ExecutionMode.SEQUENTIAL

    )

    strategy: ParallelStrategy = (

        ParallelStrategy.THREAD_POOL

    )

    # =====================================================
    # Tasks
    # =====================================================

    pending_tasks: List[str] = Field(

        default_factory=list

    )

    ready_tasks: List[str] = Field(

        default_factory=list

    )

    running_tasks: List[str] = Field(

        default_factory=list

    )

    completed_tasks: List[str] = Field(

        default_factory=list

    )

    failed_tasks: List[str] = Field(

        default_factory=list

    )

    # =====================================================
    # Task Status
    # =====================================================

    task_status: Dict[str, TaskStatus] = Field(

        default_factory=dict

    )

    # =====================================================
    # Dependencies
    # =====================================================

    dependencies: Dict[str, List[str]] = Field(

        default_factory=dict

    )

    # =====================================================
    # Workers
    # =====================================================

    workers: List[WorkerInfo] = Field(

        default_factory=list

    )

    max_workers: int = 4

    # =====================================================
    # Results
    # =====================================================

    results: Dict[str, Any] = Field(

        default_factory=dict

    )

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = Field(

        default_factory=dict

    )

    # =====================================================
    # Helpers
    # =====================================================

    def mark_running(

        self,

        task_id: str,

    ) -> None:

        self.task_status[

            task_id

        ] = TaskStatus.RUNNING

        if task_id in self.ready_tasks:

            self.ready_tasks.remove(

                task_id

            )

        if task_id not in self.running_tasks:

            self.running_tasks.append(

                task_id

            )

    def mark_completed(

        self,

        task_id: str,

        result: Any = None,

    ) -> None:

        self.task_status[

            task_id

        ] = TaskStatus.COMPLETED

        if task_id in self.running_tasks:

            self.running_tasks.remove(

                task_id

            )

        if task_id not in self.completed_tasks:

            self.completed_tasks.append(

                task_id

            )

        self.results[

            task_id

        ] = result

    def mark_failed(

        self,

        task_id: str,

        error: Any = None,

    ) -> None:

        self.task_status[

            task_id

        ] = TaskStatus.FAILED

        if task_id in self.running_tasks:

            self.running_tasks.remove(

                task_id

            )

        if task_id not in self.failed_tasks:

            self.failed_tasks.append(

                task_id

            )

        self.results[

            task_id

        ] = error