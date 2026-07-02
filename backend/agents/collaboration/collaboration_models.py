"""
Collaboration Models

Responsibilities

- Collaboration modes
- Agent roles
- Collaboration status
- Task priority

Used by

- Collaboration Agent
- Collaboration Manager
- Agent Registry
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


# ==========================================================
# Collaboration Mode
# ==========================================================

class CollaborationMode(str, Enum):

    SINGLE_AGENT = "single_agent"

    PARALLEL = "parallel"

    HIERARCHICAL = "hierarchical"

    PIPELINE = "pipeline"

    CONSENSUS = "consensus"

    VOTING = "voting"


# ==========================================================
# Collaboration Status
# ==========================================================

class CollaborationStatus(str, Enum):

    PENDING = "pending"

    ASSIGNED = "assigned"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ==========================================================
# Agent Role
# ==========================================================

class AgentRole(str, Enum):

    ORCHESTRATOR = "orchestrator"

    PLANNER = "planner"

    EXECUTOR = "executor"

    MEMORY = "memory"

    REFLECTION = "reflection"

    TOOL_SELECTOR = "tool_selector"

    REVIEWER = "reviewer"

    DOMAIN_SPECIALIST = "domain_specialist"


# ==========================================================
# Task Priority
# ==========================================================

class TaskPriority(str, Enum):

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


# ==========================================================
# Collaboration Task
# ==========================================================

class CollaborationTask(BaseModel):

    task_id: str

    task_name: str

    assigned_agent: str = ""

    role: AgentRole = (

        AgentRole.DOMAIN_SPECIALIST

    )

    priority: TaskPriority = (

        TaskPriority.MEDIUM

    )

    status: CollaborationStatus = (

        CollaborationStatus.PENDING

    )


# ==========================================================
# Collaboration Report
# ==========================================================

class CollaborationReport(BaseModel):

    mode: CollaborationMode

    total_agents: int = 0

    total_tasks: int = 0

    completed_tasks: int = 0

    failed_tasks: int = 0

    execution_time_ms: float = 0.0