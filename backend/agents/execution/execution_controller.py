"""
Execution Controller

Responsibilities

- Validate execution
- Dispatch tool execution
- Handle retries
- Record metrics
- Return standardized result

Future

- Parallel Execution
- Async Execution
- Human Approval
- Distributed Workers
"""

from __future__ import annotations

from typing import Any
from typing import Dict

from agents.execution.execution_dispatcher import (
    ExecutionDispatcher,
)

from agents.execution.execution_logger import (
    ExecutionLogger,
)

from agents.execution.execution_metrics import (
    ExecutionMetrics,
)

from agents.execution.execution_result import (
    ExecutionResult,
)

from agents.execution.execution_retry import (
    ExecutionRetry,
)

from agents.execution.execution_state import (
    ExecutionState,
)

from agents.execution.execution_validator import (
    ExecutionValidator,
)

from agents.execution.execution_models import (
    ExecutionStatus,
)

from agents.core.tool_definition import (
    ToolDefinition,
)

class ExecutionController:

    """
    Main execution engine.
    """

    def __init__(self):

        self.validator = (
            ExecutionValidator()
        )

        self.dispatcher = (
            ExecutionDispatcher()
        )

        self.retry = (
            ExecutionRetry()
        )

        self.logger = (
            ExecutionLogger()
        )

        self.metrics = (
            ExecutionMetrics()
        )

    # =====================================================
    # Execute
    # =====================================================

    async def execute(

        self,

        tool: ToolDefinition,

        provider: str,

        task_input: Dict[str, Any],

        state: ExecutionState,

    ) -> ExecutionResult:

        #
        # Populate execution state
        #

        state.tool_name = tool.name

        state.provider_name = provider

        #
        # Validation
        #

        if not self.validator.validate(

            tool,

            provider,

            state,

        ):

            self.logger.validation_failed()

            return ExecutionResult.failed(

                error="Execution validation failed.",

                tool_name=state.tool_name or "unknown",

                provider_name=provider,

            )

        #
        # Start execution
        #

        state.start()

        self.logger.execution_started(
            state
        )

        #
        # Timer
        #

        start_time = (
            self.metrics.start_timer()
        )

        #
        # Retry Loop
        #

        while True:

            try:

                output = (

                    await self.dispatcher.dispatch(

                        tool,

                        task_input,

                    )

                )

                execution_time = (

                    self.metrics.stop_timer(

                        start_time

                    )

                )

                state.complete(
                    output
                )

                state.execution_result = (
                    output
                )

                state.execution_time_ms = (
                    execution_time
                )

                self.metrics.record_success(
                    execution_time
                )

                result = (

                    ExecutionResult.completed(

                        output=output,

                        tool_name=state.tool_name,

                        provider_name=provider,

                        execution_time_ms=execution_time,

                    )

                )

                self.logger.execution_completed(
                    result
                )

                return result

            except Exception as exc:

                execution_time = (

                    self.metrics.stop_timer(

                        start_time

                    )

                )

                self.metrics.record_failure(
                    execution_time
                )

                self.logger.execution_failed(
                    str(exc)
                )

                #
                # Retry?
                #

                if self.retry.should_retry(

                    state.retry_count

                ):

                    delay = (

                        self.retry.retry_delay(

                            state.retry_count

                        )

                    )

                    self.logger.retrying(

                        state.retry_count + 1,

                        delay,

                    )

                    #
                    # Future:
                    #
                    # time.sleep(delay)
                    #

                    state.retry()

                    continue

                #
                # Final Failure
                #

                state.fail(
                    str(exc)
                )

                return ExecutionResult.failed(

                    error=str(exc),

                    tool_name=state.tool_name or "unknown",

                    provider_name=provider,

                    retry_count=state.retry_count,

                )