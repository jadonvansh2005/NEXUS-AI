"""
Worker Pool

Responsibilities

- Execute tasks in parallel
- Manage worker threads
- Collect execution results
- Handle worker failures

Future

- AsyncIO
- Celery
- Ray
- Kubernetes Workers
"""

from __future__ import annotations

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from typing import Any
from typing import Callable
from typing import Dict


class WorkerPool:

    """
    Executes tasks using a thread pool.
    """

    def __init__(

        self,

        max_workers: int = 4,

    ):

        self.max_workers = max_workers

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        task_map: Dict[str, Callable[[], Any]],

    ) -> Dict[str, Any]:

        """
        Parameters
        ----------
        task_map

            {

                task_id: callable

            }

        Returns
        -------
        {

            task_id: result

        }
        """

        results: Dict[str, Any] = {}

        future_map = {}

        with ThreadPoolExecutor(

            max_workers=self.max_workers,

        ) as executor:

            #
            # Submit Tasks
            #

            for task_id, task in task_map.items():

                future = executor.submit(

                    task

                )

                future_map[

                    future

                ] = task_id

            #
            # Collect Results
            #

            for future in as_completed(

                future_map

            ):

                task_id = future_map[

                    future

                ]

                try:

                    results[

                        task_id

                    ] = future.result()

                except Exception as error:

                    results[

                        task_id

                    ] = error

        return results

    # =====================================================
    # Worker Count
    # =====================================================

    def worker_count(

        self,

    ) -> int:

        return self.max_workers

    # =====================================================
    # Update Workers
    # =====================================================

    def set_workers(

        self,

        workers: int,

    ) -> None:

        self.max_workers = max(

            1,

            workers,

        )