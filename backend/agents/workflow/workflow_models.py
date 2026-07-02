"""
Workflow Models

Internal workflow models, enums and configuration.

Used by

- Workflow Agent
- Workflow Builder
- Workflow Scheduler
- Workflow Executor
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Workflow Status
# ==========================================================

class WorkflowStatus(str, Enum):

    CREATED = "created"

    READY = "ready"

    RUNNING = "running"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ==========================================================
# Task Status
# ==========================================================

class WorkflowTaskStatus(str, Enum):

    PENDING = "pending"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"

    WAITING = "waiting"


# ==========================================================
# Workflow Type
# ==========================================================

class WorkflowType(str, Enum):

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

    CONDITIONAL = "conditional"

    HYBRID = "hybrid"


# ==========================================================
# Dependency Type
# ==========================================================

class DependencyType(str, Enum):

    HARD = "hard"

    SOFT = "soft"


# ==========================================================
# Retry Policy
# ==========================================================

class RetryPolicy(str, Enum):

    NEVER = "never"

    ONCE = "once"

    ALWAYS = "always"


# ==========================================================
# Workflow Configuration
# ==========================================================

class WorkflowConfiguration(BaseModel):

    max_parallel_tasks: int = 5

    max_retry_attempts: int = 3

    allow_parallel_execution: bool = True

    enable_checkpointing: bool = True

    enable_logging: bool = True

    enable_reflection: bool = True

    retry_policy: RetryPolicy = RetryPolicy.ONCE