"""
Execution Scheduler

Responsibilities

- Schedule ready tasks
- Assign tasks to workers
- Respect worker limits
- Prepare execution batches

Future

- Priority Scheduling
- Resource-Aware Scheduling
- GPU Scheduling
- Distributed Scheduling
"""

from __future__ import annotations

from typing import Dict
from typing import List

from agents.parallel_execution.parallel_models import (
    WorkerStatus,
)

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


class ExecutionScheduler:

    """
    Assign ready tasks to available workers.
    """

    # =====================================================
    # Schedule
    # =====================================================

    def schedule(

        self,

        state: ParallelState,

    ) -> Dict[str, List[str]]:

        assignments: Dict[str, List[str]] = {}

        #
        # Available workers
        #

        available_workers = [

            worker

            for worker

            in state.workers

            if worker.status == WorkerStatus.IDLE

        ]

        if not available_workers:

            return assignments

        ready_tasks = list(

            state.ready_tasks

        )

        worker_index = 0

        #
        # Round Robin Scheduling
        #

        for task in ready_tasks:

            if worker_index >= len(

                available_workers

            ):

                break

            worker = available_workers[

                worker_index

            ]

            assignments.setdefault(

                worker.worker_id,

                [],

            ).append(

                task

            )

            worker.current_task = task

            worker.status = (

                WorkerStatus.RUNNING

            )

            worker_index += 1

        return assignments

    # =====================================================
    # Idle Workers
    # =====================================================

    def idle_workers(

        self,

        state: ParallelState,

    ):

        return [

            worker

            for worker

            in state.workers

            if worker.status == WorkerStatus.IDLE

        ]

    # =====================================================
    # Busy Workers
    # =====================================================

    def busy_workers(

        self,

        state: ParallelState,

    ):

        return [

            worker

            for worker

            in state.workers

            if worker.status == WorkerStatus.RUNNING

        ]

    # =====================================================
    # Has Capacity
    # =====================================================

    def has_capacity(

        self,

        state: ParallelState,

    ) -> bool:

        return len(

            self.idle_workers(

                state

            )

        ) > 0