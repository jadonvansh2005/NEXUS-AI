"""
Execution Metrics

Responsibilities

- Track execution metrics
- Measure execution time
- Count successes and failures
- Provide execution statistics

Future

- Prometheus
- Grafana
- OpenTelemetry
- Cost Metrics
"""

from __future__ import annotations

import time

from typing import Dict


class ExecutionMetrics:

    """
    Collects execution statistics.
    """

    def __init__(self):

        self.total_executions = 0

        self.successful_executions = 0

        self.failed_executions = 0

        self.total_execution_time = 0.0

    # =====================================================
    # Timer
    # =====================================================

    def start_timer(
        self,
    ) -> float:

        return time.perf_counter()

    def stop_timer(
        self,
        start_time: float,
    ) -> float:

        return (

            time.perf_counter()

            - start_time

        ) * 1000

    # =====================================================
    # Record Success
    # =====================================================

    def record_success(
        self,
        execution_time_ms: float,
    ) -> None:

        self.total_executions += 1

        self.successful_executions += 1

        self.total_execution_time += (

            execution_time_ms

        )

    # =====================================================
    # Record Failure
    # =====================================================

    def record_failure(
        self,
        execution_time_ms: float,
    ) -> None:

        self.total_executions += 1

        self.failed_executions += 1

        self.total_execution_time += (

            execution_time_ms

        )

    # =====================================================
    # Average Execution Time
    # =====================================================

    @property
    def average_execution_time(
        self,
    ) -> float:

        if self.total_executions == 0:

            return 0.0

        return (

            self.total_execution_time

            / self.total_executions

        )

    # =====================================================
    # Success Rate
    # =====================================================

    @property
    def success_rate(
        self,
    ) -> float:

        if self.total_executions == 0:

            return 0.0

        return (

            self.successful_executions

            / self.total_executions

        ) * 100

    # =====================================================
    # Failure Rate
    # =====================================================

    @property
    def failure_rate(
        self,
    ) -> float:

        if self.total_executions == 0:

            return 0.0

        return (

            self.failed_executions

            / self.total_executions

        ) * 100

    # =====================================================
    # Export Metrics
    # =====================================================

    def export(
        self,
    ) -> Dict:

        return {

            "total_executions": self.total_executions,

            "successful_executions": self.successful_executions,

            "failed_executions": self.failed_executions,

            "average_execution_time_ms": (

                round(

                    self.average_execution_time,

                    2,

                )

            ),

            "success_rate": round(

                self.success_rate,

                2,

            ),

            "failure_rate": round(

                self.failure_rate,

                2,

            ),

        }