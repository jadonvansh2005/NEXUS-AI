"""
Execution Retry

Responsibilities

- Retry failed executions
- Determine retry eligibility
- Calculate retry delay

Future

- Exponential Backoff
- Provider-aware Retry
- Reflection-based Retry
- Circuit Breaker
"""

from __future__ import annotations

from agents.execution.execution_models import (
    RetryPolicy,
)


class ExecutionRetry:

    """
    Handles retry decisions for execution failures.
    """

    def __init__(

        self,

        max_retries: int = 3,

        retry_policy: RetryPolicy = (
            RetryPolicy.EXPONENTIAL_BACKOFF
        ),

    ):

        self.max_retries = max_retries

        self.retry_policy = retry_policy

    # =====================================================
    # Should Retry
    # =====================================================

    def should_retry(

        self,

        retry_count: int,

    ) -> bool:

        return retry_count < self.max_retries

    # =====================================================
    # Retry Delay
    # =====================================================

    def retry_delay(

        self,

        retry_count: int,

    ) -> float:

        #
        # Never Retry
        #

        if self.retry_policy == RetryPolicy.NEVER:

            return 0.0

        #
        # Immediate Retry
        #

        if self.retry_policy == RetryPolicy.IMMEDIATE:

            return 0.0

        #
        # Exponential Backoff
        #

        return float(

            2 ** retry_count

        )

    # =====================================================
    # Reset
    # =====================================================

    def reset(

        self,

    ) -> int:

        return 0

    # =====================================================
    # Next Retry Count
    # =====================================================

    def increment(

        self,

        retry_count: int,

    ) -> int:

        return retry_count + 1