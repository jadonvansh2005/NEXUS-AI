"""
Agent Registry

Responsibilities

- Register available agents
- Retrieve agents
- Check agent availability
- List registered agents

Future

- Dynamic Agent Discovery
- Remote Agents
- Agent Versioning
- Health Monitoring
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional

from agents.core.base_agent import (
    BaseAgent,
)


class AgentRegistry:

    """
    Registry for all available agents.
    """

    def __init__(

        self,

    ):

        self._agents: Dict[str, BaseAgent] = {}

    # =====================================================
    # Register
    # =====================================================

    def register(

        self,

        name: str,

        agent: BaseAgent,

    ) -> None:

        self._agents[

            name

        ] = agent

    # =====================================================
    # Unregister
    # =====================================================

    def unregister(

        self,

        name: str,

    ) -> None:

        self._agents.pop(

            name,

            None,

        )

    # =====================================================
    # Get
    # =====================================================

    def get(

        self,

        name: str,

    ) -> Optional[BaseAgent]:

        return self._agents.get(

            name

        )

    # =====================================================
    # Exists
    # =====================================================

    def exists(

        self,

        name: str,

    ) -> bool:

        return name in self._agents

    # =====================================================
    # List
    # =====================================================

    def list_agents(

        self,

    ) -> List[str]:

        return list(

            self._agents.keys()

        )

    # =====================================================
    # Count
    # =====================================================

    def count(

        self,

    ) -> int:

        return len(

            self._agents

        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(

        self,

    ) -> None:

        self._agents.clear()