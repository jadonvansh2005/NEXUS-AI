"""
Parallel Manager

Responsibilities

- Coordinate parallel execution
- Validate execution state
- Analyze dependencies
- Schedule tasks
- Execute workers
- Collect results

Future

- Distributed Execution
- Dynamic Worker Scaling
- Retry Policies
- Fault Tolerance
"""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Dict

from agents.parallel_execution.dependency_analyzer import (
    DependencyAnalyzer,
)

from agents.parallel_execution.execution_scheduler import (
    ExecutionScheduler,
)

from agents.parallel_execution.parallel_logger import (
    ParallelLogger,
)

from agents.parallel_execution.parallel_state import (
    ParallelState,
)

from agents.parallel_execution.parallel_validator import (
    ParallelValidator,
)

from agents.parallel_execution.result_collector import (
    ResultCollector,
)

from agents.parallel_execution.worker_pool import (
    WorkerPool,
)


class ParallelManager:

    """
    Coordinates the complete
    parallel execution pipeline.
    """

    def __init__(

        self,

    ):

        self.validator = (

            ParallelValidator()

        )

        self.analyzer = (

            DependencyAnalyzer()

        )

        self.scheduler = (

            ExecutionScheduler()

        )

        self.collector = (

            ResultCollector()

        )

        self.logger = (

            ParallelLogger()

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: ParallelState,

        task_map: Dict[str, Callable[[], Any]],

    ) -> ParallelState:

        #
        # Validate
        #

        if not self.validator.validate(

            state

        ):

            self.logger.validation_failed()

            return state

        #
        # Start
        #

        self.logger.execution_started(

            state

        )

        #
        # Analyze Dependencies
        #

        state = self.analyzer.analyze(

            state

        )

        #
        # Schedule Tasks
        #

        assignments = self.scheduler.schedule(

            state

        )

        #
        # Log assignments
        #

        executable_tasks: Dict[str, Callable[[], Any]] = {}

        for worker_id, task_ids in assignments.items():

            for task_id in task_ids:

                self.logger.task_scheduled(

                    worker_id,

                    task_id,

                )

                state.mark_running(

                    task_id

                )

                if task_id in task_map:

                    executable_tasks[

                        task_id

                    ] = task_map[

                        task_id

                    ]

        #
        # Execute Tasks
        #

        worker_pool = WorkerPool(

            max_workers=state.max_workers

        )

        worker_results = worker_pool.execute(

            executable_tasks

        )

        #
        # Collect Results
        #

        state = self.collector.collect(

            state,

            worker_results,

        )

        #
        # Log Results
        #

        for task_id in state.completed_tasks:

            self.logger.task_completed(

                task_id

            )

        for task_id in state.failed_tasks:

            error = str(

                state.results.get(

                    task_id,

                    "",

                )

            )

            self.logger.task_failed(

                task_id,

                error,

            )

        #
        # Finished
        #

        self.logger.execution_completed(

            state

        )

        return state