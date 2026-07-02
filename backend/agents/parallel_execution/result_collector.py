"""
Result Collector

Responsibilities

- Collect worker results
- Merge execution outputs
- Track execution statistics
- Prepare final execution result

Future

- Streaming Results
- Partial Result Handling
- Result Ranking
- Result Compression
"""

from __future__ import annotations

from typing import Any
from typing import Dict

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


class ResultCollector:

    """
    Collects and merges results
    from parallel workers.
    """

    # =====================================================
    # Collect Results
    # =====================================================

    def collect(

        self,

        state: ParallelState,

        worker_results: Dict[str, Any],

    ) -> ParallelState:

        for task_id, result in worker_results.items():

            #
            # Store Result
            #

            state.results[

                task_id

            ] = result

            #
            # Successful execution
            #

            if not isinstance(

                result,

                Exception,

            ):

                state.mark_completed(

                    task_id,

                    result,

                )

            #
            # Failed execution
            #

            else:

                state.mark_failed(

                    task_id,

                    str(result),

                )

        return state

    # =====================================================
    # Successful Results
    # =====================================================

    def successful_results(

        self,

        state: ParallelState,

    ) -> Dict[str, Any]:

        return {

            task: state.results[task]

            for task in state.completed_tasks

            if task in state.results

        }

    # =====================================================
    # Failed Results
    # =====================================================

    def failed_results(

        self,

        state: ParallelState,

    ) -> Dict[str, Any]:

        return {

            task: state.results[task]

            for task in state.failed_tasks

            if task in state.results

        }

    # =====================================================
    # Summary
    # =====================================================

    def summary(

        self,

        state: ParallelState,

    ) -> Dict[str, int]:

        return {

            "completed": len(

                state.completed_tasks

            ),

            "failed": len(

                state.failed_tasks

            ),

            "running": len(

                state.running_tasks

            ),

            "pending": len(

                state.pending_tasks

            ),

        }