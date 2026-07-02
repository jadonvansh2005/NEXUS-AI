"""
Parallel Execution Models

Responsibilities

- Execution modes
- Worker status
- Task status
- Parallel strategy

Used by

- Parallel Agent
- Parallel Manager
- Execution Controller
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Execution Mode
# ==========================================================

class ExecutionMode(str, Enum):

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

    HYBRID = "hybrid"


# ==========================================================
# Worker Status
# ==========================================================

class WorkerStatus(str, Enum):

    IDLE = "idle"

    RUNNING = "running"

    WAITING = "waiting"

    COMPLETED = "completed"

    FAILED = "failed"


# ==========================================================
# Task Status
# ==========================================================

class TaskStatus(str, Enum):

    PENDING = "pending"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"


# ==========================================================
# Parallel Strategy
# ==========================================================

class ParallelStrategy(str, Enum):

    THREAD_POOL = "thread_pool"

    ASYNC_IO = "asyncio"

    PROCESS_POOL = "process_pool"

    CELERY = "celery"

    RAY = "ray"


# ==========================================================
# Worker Information
# ==========================================================

class WorkerInfo(BaseModel):

    worker_id: str

    status: WorkerStatus = (

        WorkerStatus.IDLE

    )

    current_task: str = ""

    completed_tasks: int = 0


# ==========================================================
# Parallel Report
# ==========================================================

class ParallelReport(BaseModel):

    execution_mode: ExecutionMode

    strategy: ParallelStrategy

    total_tasks: int

    completed_tasks: int = 0

    failed_tasks: int = 0

    execution_time_ms: float = 0.0