"""
Reflection Models

Responsibilities

- Reflection status
- Reflection type
- Confidence level
- Reflection result

Used by

- Reflection Agent
- Reflection Manager
- Execution Controller
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Reflection Status
# ==========================================================

class ReflectionStatus(str, Enum):

    NOT_REQUIRED = "not_required"

    PENDING = "pending"

    COMPLETED = "completed"

    FAILED = "failed"


# ==========================================================
# Reflection Type
# ==========================================================

class ReflectionType(str, Enum):

    NONE = "none"

    TOOL_SELECTION = "tool_selection"

    PROVIDER_SELECTION = "provider_selection"

    EXECUTION = "execution"

    RESPONSE = "response"

    PLANNING = "planning"

    MEMORY = "memory"

    WORKFLOW = "workflow"


# ==========================================================
# Confidence Level
# ==========================================================

class ConfidenceLevel(str, Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    VERY_HIGH = "very_high"


# ==========================================================
# Reflection Result
# ==========================================================

class ReflectionResult(str, Enum):

    SUCCESS = "success"

    RETRY = "retry"

    FALLBACK = "fallback"

    REPLAN = "replan"

    ESCALATE = "escalate"

    FAIL = "fail"


# ==========================================================
# Reflection Report
# ==========================================================

class ReflectionReport(BaseModel):

    reflection_type: ReflectionType

    status: ReflectionStatus = (

        ReflectionStatus.PENDING

    )

    confidence: ConfidenceLevel = (

        ConfidenceLevel.MEDIUM

    )

    result: ReflectionResult = (

        ReflectionResult.SUCCESS

    )

    summary: str = ""

    recommendation: str = ""

    improvement: str = ""