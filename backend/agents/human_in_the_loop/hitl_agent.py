"""
Human-in-the-Loop Agent

Responsibilities

- Orchestrate approval workflow
- Delegate approval decisions
- Return approval state

Future

- Web Approval
- Mobile Approval
- Slack Approval
- Teams Approval
- Email Approval
"""

from __future__ import annotations

from agents.core.base_agent import (
    BaseAgent,
)

from agents.core.agent_state import (
    AgentState,
)

from agents.human_in_the_loop.approval_manager import (
    ApprovalManager,
)

from agents.human_in_the_loop.approval_models import (
    ApprovalAction,
    RiskLevel,
)

from agents.human_in_the_loop.approval_state import (
    ApprovalState,
)


class HITLAgent(

    BaseAgent

):

    """
    Human-in-the-Loop Agent.
    """

    def __init__(

        self,

    ):

        super().__init__(

            "HITLAgent"

        )

        self.manager = (

            ApprovalManager()

        )

    # =====================================================
    # Execute
    # =====================================================

    def execute(

        self,

        state: AgentState,

    ) -> AgentState:

        self.log(

            "Starting Human-in-the-Loop"

        )

        #
        # Future:
        # Planner / Execution Controller
        # will provide the actual action
        #

        action = ApprovalAction.EXECUTE

        approval_state = (

            ApprovalState(

                user_id=state.user_id or 0,

                task_id="task_1",

                query=state.user_query,

                action=action,

                risk_level=RiskLevel.LOW,

            )

        )

        approval_state = (

            self.manager.process(

                approval_state

            )

        )

        #
        # Store approval state
        #

        state.metadata[

            "approval_status"

        ] = approval_state.status.value

        state.metadata[

            "approval_required"

        ] = (

            approval_state.status.value

            == "pending"

        )

        return state