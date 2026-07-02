"""
Execution Result

Responsibilities

- Standardize tool execution output
- Capture execution metadata
- Return execution status

Future

- Streaming Results
- Cost Tracking
- Token Usage
- Provider Metrics
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


class ExecutionResult(BaseModel):
    """
    Standard execution result returned by every tool.
    """

    #
    # Status
    #

    status: ExecutionStatus

    #
    # Output
    #

    output: Optional[Any] = None

    #
    # Error
    #

    error: Optional[str] = None

    #
    # Execution Metadata
    #

    tool_name: Optional[str] = None

    provider_name: Optional[str] = None

    execution_time_ms: float = 0.0

    retry_count: int = 0

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    # =====================================================
    # Helpers
    # =====================================================

    @property
    def success(
        self,
    ) -> bool:

        return self.status == (
            ExecutionStatus.COMPLETED
        )

    @property
    def failed(
        self,
    ) -> bool:

        return self.status == (
            ExecutionStatus.FAILED
        )

    @classmethod
    def completed(
        cls,
        output: Any,
        tool_name: str,
        provider_name: str,
        execution_time_ms: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None,
    ):

        return cls(

            status=ExecutionStatus.COMPLETED,

            output=output,

            tool_name=tool_name,

            provider_name=provider_name,

            execution_time_ms=execution_time_ms,

            metadata=metadata or {},

        )

    @classmethod
    def failed(
        cls,
        error: str,
        tool_name: str,
        provider_name: str,
        retry_count: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ):

        return cls(

            status=ExecutionStatus.FAILED,

            error=error,

            tool_name=tool_name,

            provider_name=provider_name,

            retry_count=retry_count,

            metadata=metadata or {},

        )