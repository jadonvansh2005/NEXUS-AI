"""
UPSS Tool SDK - Tool Context

Provides runtime context shared by every tool execution.

The ToolContext contains everything a tool needs to execute
without directly depending on the Orchestrator or AgentState.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ToolContext:
    """
    Runtime context available to every tool.
    """

    # ==========================================================
    # User Information
    # ==========================================================

    user_id: str = "1"

    session_id: str = "session"

    conversation_id: str = "conversation"

    # ==========================================================
    # Runtime Objects
    # ==========================================================

    agent_state: Any = None

    planner_output: Any = None

    memory: Any = None

    settings: Any = None

    logger: Any = None

    # ==========================================================
    # Execution Information
    # ==========================================================

    request_id: str | None = None

    parent_tool: str | None = None

    execution_depth: int = 0

    started_at: datetime = field(default_factory=datetime.utcnow)

    # ==========================================================
    # Shared Storage
    # ==========================================================

    shared_data: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def set(self, key: str, value: Any) -> None:
        """
        Store a runtime value.
        """
        self.shared_data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a runtime value.
        """
        return self.shared_data.get(key, default)

    def update_metadata(self, **kwargs: Any) -> None:
        """
        Update execution metadata.
        """
        self.metadata.update(kwargs)

    def clone(self) -> "ToolContext":
        """
        Create a shallow copy of the context.

        Useful when a tool invokes another tool.
        """

        return ToolContext(
            user_id=self.user_id,
            session_id=self.session_id,
            conversation_id=self.conversation_id,
            agent_state=self.agent_state,
            planner_output=self.planner_output,
            memory=self.memory,
            settings=self.settings,
            logger=self.logger,
            request_id=self.request_id,
            parent_tool=self.parent_tool,
            execution_depth=self.execution_depth + 1,
            shared_data=self.shared_data.copy(),
            metadata=self.metadata.copy(),
        )