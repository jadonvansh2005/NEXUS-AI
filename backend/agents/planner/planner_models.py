"""
Planner Models

Internal planner models, enums and constants.

Used by:

- Planner
- Planner Validator
- Planner Rules
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Complexity
# ==========================================================

class ComplexityLevel(str, Enum):

    SIMPLE = "simple"

    MEDIUM = "medium"

    COMPLEX = "complex"


# ==========================================================
# Risk
# ==========================================================

class RiskLevel(str, Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"


# ==========================================================
# Task Status
# ==========================================================

class PlannerTaskStatus(str, Enum):

    PENDING = "pending"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"


# ==========================================================
# Task Type
# ==========================================================

class PlannerTaskType(str, Enum):

    TOOL = "tool"

    AGENT = "agent"

    MEMORY = "memory"

    VALIDATION = "validation"

    APPROVAL = "approval"

    RESPONSE = "response"


# ==========================================================
# Execution Strategy
# ==========================================================

class ExecutionStrategy(str, Enum):

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

    HYBRID = "hybrid"


# ==========================================================
# Planner Configuration
# ==========================================================

class PlannerConfiguration(BaseModel):

    max_tasks: int = 25

    max_parallel_tasks: int = 5

    allow_parallel_execution: bool = True

    allow_human_approval: bool = True

    enable_reflection: bool = True

    enable_retry: bool = True

    default_strategy: ExecutionStrategy = (
        ExecutionStrategy.SEQUENTIAL
    )