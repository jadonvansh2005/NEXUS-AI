"""
Reflection State

Responsibilities

- Runtime reflection state
- Execution metadata
- Reflection output
- Improvement suggestions

Future

- LLM Reflection
- User Feedback
- Multi-Agent Reflection
"""

from __future__ import annotations

from typing import Any
from typing import Dict

from pydantic import BaseModel
from pydantic import Field

from agents.reflection.reflection_models import (
    ConfidenceLevel,
    ReflectionResult,
    ReflectionStatus,
    ReflectionType,
)


class ReflectionState(BaseModel):
    """
    Runtime state for Reflection Agent.
    """

    # =====================================================
    # User
    # =====================================================

    user_id: int

    query: str

    # =====================================================
    # Execution Information
    # =====================================================

    task_id: str = ""

    tool_name: str = ""

    provider_name: str = ""

    execution_success: bool = True

    execution_time_ms: float = 0.0

    # =====================================================
    # LLM Response
    # =====================================================

    response: str = ""

    # =====================================================
    # Reflection
    # =====================================================

    reflection_type: ReflectionType = (

        ReflectionType.NONE

    )

    status: ReflectionStatus = (

        ReflectionStatus.PENDING

    )

    confidence: ConfidenceLevel = (

        ConfidenceLevel.MEDIUM

    )

    result: ReflectionResult = (

        ReflectionResult.SUCCESS

    )

    # =====================================================
    # Reflection Output
    # =====================================================

    summary: str = ""

    recommendation: str = ""

    improvement: str = ""

    # =====================================================
    # Metadata
    # =====================================================

    metadata: Dict[str, Any] = Field(

        default_factory=dict

    )

    # =====================================================
    # Helpers
    # =====================================================

    def complete(

        self,

        summary: str,

        recommendation: str = "",

        improvement: str = "",

    ) -> None:

        self.summary = summary

        self.recommendation = recommendation

        self.improvement = improvement

        self.status = ReflectionStatus.COMPLETED

    def fail(

        self,

        reason: str,

    ) -> None:

        self.status = ReflectionStatus.FAILED

        self.summary = reason