"""
Execution Models

Responsibilities

- Execution status
- Execution mode
- Retry policy
- Execution configuration

Used by

- Execution Controller
- Dispatcher
- Validator
- Retry Engine
- Metrics
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Execution Status
# ==========================================================

class ExecutionStatus(str, Enum):

    CREATED = "created"

    READY = "ready"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    RETRYING = "retrying"


# ==========================================================
# Execution Mode
# ==========================================================

class ExecutionMode(str, Enum):

    SYNCHRONOUS = "synchronous"

    ASYNCHRONOUS = "asynchronous"

    PARALLEL = "parallel"


# ==========================================================
# Retry Policy
# ==========================================================

class RetryPolicy(str, Enum):

    NEVER = "never"

    IMMEDIATE = "immediate"

    EXPONENTIAL_BACKOFF = "exponential_backoff"


# ==========================================================
# Execution Priority
# ==========================================================

class ExecutionPriority(str, Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Error Severity
# ==========================================================

class ErrorSeverity(str, Enum):

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"


# ==========================================================
# Execution Configuration
# ==========================================================

class ExecutionConfiguration(BaseModel):

    timeout_seconds: int = 60

    max_retry_attempts: int = 3

    enable_retry: bool = True

    enable_metrics: bool = True

    enable_logging: bool = True

    enable_validation: bool = True

    execution_mode: ExecutionMode = (
        ExecutionMode.SYNCHRONOUS
    )

    retry_policy: RetryPolicy = (
        RetryPolicy.EXPONENTIAL_BACKOFF
    )