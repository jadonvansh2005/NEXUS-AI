"""
Parallel Execution Agent

Responsibilities

- Orchestrate parallel execution
- Delegate execution to Parallel Manager
- Store execution results

Future

- Distributed Execution
- Dynamic Scaling
- Retry Strategies
- Cloud Workers
"""

from __future__ import annotations

from typing import Any
from typing import Callable
from typing import Dict

from agents.core.base_agent import (
    BaseAgent,
)

from agents.core.agent_state import (
    AgentState,
)

from agents.parallel_execution.parallel_manager import (
    ParallelManager,
)

from agents.parallel_execution.parallel_models import (
    ExecutionMode,
    ParallelStrategy,
    WorkerInfo,
)

from agents.parallel_execution.parallel_state import (
    ParallelState,
)


class ParallelAgent(

    BaseAgent

):

    """
    Parallel Execution Agent.
    """

    def __init__(

        self,

    ):

        super().__init__(

            "ParallelAgent"

        )

        self.manager = (

            ParallelManager()

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: AgentState,

        task_map: Dict[str, Callable[[], Any]],

    ) -> AgentState:

        self.log(

            "Starting Parallel Execution"

        )

        #
        # Build Parallel State
        #

        parallel_state = (

            ParallelState(

                workflow_id=state.metadata.get(

                    "workflow_id",

                    "",

                ),

                execution_mode=ExecutionMode.PARALLEL,

                strategy=ParallelStrategy.THREAD_POOL,

                pending_tasks=list(

                    task_map.keys()

                ),

                dependencies=state.metadata.get(

                    "task_dependencies",

                    {},

                ),

                max_workers=state.metadata.get(

                    "max_workers",

                    4,

                ),

                workers=[

                    WorkerInfo(

                        worker_id=f"worker_{i+1}"

                    )

                    for i in range(

                        state.metadata.get(

                            "max_workers",

                            4,

                        )

                    )

                ],

            )

        )

        #
        # Execute Parallel Workflow
        #

        parallel_state = (

            self.manager.execute(

                parallel_state,

                task_map,

            )

        )

        #
        # Save Results
        #

        state.metadata[

            "parallel_execution_mode"

        ] = (

            parallel_state.execution_mode.value

        )

        state.metadata[

            "parallel_strategy"

        ] = (

            parallel_state.strategy.value

        )

        state.metadata[

            "parallel_completed_tasks"

        ] = (

            parallel_state.completed_tasks

        )

        state.metadata[

            "parallel_failed_tasks"

        ] = (

            parallel_state.failed_tasks

        )

        state.metadata[

            "parallel_results"

        ] = (

            parallel_state.results

        )

        state.tool_outputs.update(

            parallel_state.results

        )

        return state