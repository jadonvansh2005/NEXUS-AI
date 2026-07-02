"""
Integration Bootstrap

Responsibilities

- Create Pipeline Context
- Register runtime services
- Register pipeline stages
- Build Pipeline Manager

Notes

- Composition Root of UPSS.
- Only place where objects are instantiated.
- Contains NO business logic.
"""

from __future__ import annotations

from integration.pipeline_context import (
    PipelineContext,
)

from integration.pipeline_manager import (
    PipelineManager,
)

from integration.stage_registry import (
    StageRegistry,
)

# ---------------------------------------------------------
# Stages
# ---------------------------------------------------------

from integration.stages.planner_stage import (
    PlannerStage,
)

from integration.stages.memory_stage import (
    MemoryStage,
)

from integration.stages.workflow_stage import (
    WorkflowStage,
)

from integration.stages.agent_stage import (
    AgentStage,
)

from integration.stages.tool_stage import (
    ToolStage,
)

from integration.stages.execution_stage import (
    ExecutionStage,
)

from integration.stages.reflection_stage import (
    ReflectionStage,
)

from integration.stages.validation_stage import (
    ValidationStage,
)

from integration.stages.hitl_stage import (
    HITLStage,
)

from integration.stages.response_stage import (
    ResponseStage,
)

from integration.stages.memory_writer_stage import (
    MemoryWriterStage,
)

# ---------------------------------------------------------
# Existing Services
# ---------------------------------------------------------

from agents.planner.planner_agent import (
    PlannerAgent,
)

from agents.memory_agent.memory_agent import (
    MemoryAgent,
)

from workflow.workflow_engine import (
    WorkflowEngine,
)

from agents.collaboration.collaboration_agent import (
    CollaborationAgent,
)

from tools.selector.tool_selector import (
    ToolSelector,
)

from agents.execution.execution_controller import (
    ExecutionController,
)

from agents.reflection.reflection_agent import (
    ReflectionAgent,
)

from validation.validation_manager import (
    ValidationManager,
)

from agents.human_in_the_loop.hitl_agent import (
    HITLAgent,
)

from response.response_generator import (
    ResponseGenerator,
)

from agents.memory_agent.memory_writer import (
    MemoryWriter,
)


class IntegrationBootstrap:

    """
    Creates the complete UPSS runtime.
    """

    def build(

        self,

        database,

    ) -> PipelineManager:

        #
        # --------------------------------------------------
        # Pipeline Context
        # --------------------------------------------------
        #

        context = PipelineContext(

            database=database,

        )

        #
        # --------------------------------------------------
        # Register Runtime Services
        # --------------------------------------------------
        #

        context.register(
            "planner",
            PlannerAgent(),
        )

        context.register(
            "memory_gateway",
            MemoryAgent(),
        )

        context.register(
            "workflow",
            WorkflowEngine(),
        )

        context.register(
            "agent_generator",
            CollaborationAgent(),
        )

        context.register(
            "tool_selector",
            ToolSelector(),
        )

        context.register(
            "execution_controller",
            ExecutionController(),
        )

        context.register(
            "reflection",
            ReflectionAgent(),
        )

        context.register(
            "validator",
            ValidationManager(),
        )

        context.register(
            "hitl",
            HITLAgent(),
        )

        context.register(
            "response_generator",
            ResponseGenerator(),
        )

        context.register(
            "memory_writer",
            MemoryWriter(),
        )

        #
        # --------------------------------------------------
        # Stage Registry
        # --------------------------------------------------
        #

        registry = StageRegistry()

        registry.register(

            PlannerStage()

        )

        registry.register(

            MemoryStage()

        )

        registry.register(

            WorkflowStage()

        )

        registry.register(

            AgentStage()

        )

        registry.register(

            ToolStage()

        )

        registry.register(

            ExecutionStage()

        )

        registry.register(

            ReflectionStage()

        )

        registry.register(

            ValidationStage()

        )

        registry.register(

            HITLStage()

        )

        registry.register(

            ResponseStage()

        )

        registry.register(

            MemoryWriterStage()

        )

        #
        # --------------------------------------------------
        # Pipeline Manager
        # --------------------------------------------------
        #

        return PipelineManager(

            registry=registry,

            context=context,

        )