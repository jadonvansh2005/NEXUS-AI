"""
Execution Validator

Responsibilities

- Validate execution request
- Validate selected tool
- Validate provider
- Validate execution state

Future

- Permission Validation
- Quota Validation
- Rate Limit Validation
- User Authorization
"""

from __future__ import annotations

from typing import Any
from typing import Dict
from typing import Optional

from agents.execution.execution_state import (
    ExecutionState,
)

from agents.execution.execution_models import (
    ExecutionStatus,
)


class ExecutionValidator:

    """
    Validate execution before dispatch.
    """

    # =====================================================
    # Public API
    # =====================================================

    def validate(

        self,

        tool: Optional[Dict[str, Any]],

        provider: Optional[str],

        state: ExecutionState,

    ) -> bool:

        if not self._validate_tool(tool):

            return False

        if not self._validate_provider(provider):

            return False

        if not self._validate_state(state):

            return False

        return True

    # =====================================================
    # Tool Validation
    # =====================================================

    def _validate_tool(

        self,

        tool: Optional[Any],

    ) -> bool:

        if tool is None:

            return False

        from agents.core.tool_definition import ToolDefinition
        if isinstance(tool, ToolDefinition):
            if not tool.enabled:
                return False
            if not tool.metadata or "instance" not in tool.metadata:
                return False
            return True

        if hasattr(tool, "get"):
            if not tool.get("enabled", False):
                return False
            if "tool" not in tool:
                return False
            return True

        return False

    # =====================================================
    # Provider Validation
    # =====================================================

    def _validate_provider(

        self,

        provider: Optional[str],

    ) -> bool:

        if provider is None:

            return False

        return True

    # =====================================================
    # Execution State Validation
    # =====================================================

    def _validate_state(

        self,

        state: ExecutionState,

    ) -> bool:

        if state.status not in [

            ExecutionStatus.CREATED,

            ExecutionStatus.READY,

            ExecutionStatus.RETRYING,

        ]:

            return False

        return True