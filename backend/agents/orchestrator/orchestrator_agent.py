from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState

from agents.domain_detector.detector import (
    DomainDetector
)

from agents.planner.planner_agent import (
    PlannerAgent
)

from agents.reporting_agent.reporting_agent import (
    ReportingAgent
)

from agents.orchestrator.routing_engine import (
    RoutingEngine
)

from agents.orchestrator.execution_controller import (
    ExecutionController
)

from agents.agent_factory.dynamic_generator import (
    AgentFactory
)

from agents.memory_agent.memory_agent import (
    MemoryAgent
)


class OrchestratorAgent(
    BaseAgent
):

    def __init__(self):

        super().__init__(
            "Orchestrator"
        )

        self.router = RoutingEngine()

        self.detector = DomainDetector()

        self.planner = PlannerAgent()

        self.reporter = ReportingAgent()

        self.controller = (
            ExecutionController()
        )

        self.registry = (
            AgentFactory.build()
        )

        self.memory = (

            MemoryAgent()

        )

        print(
            "\n========== AGENTS =========="
        )

        for domain, agent in self.registry.agents.items():

            print(
                domain,
                "->",
                agent.__class__.__name__
            )

        print(
            "============================\n"
        )

    async def execute(

        self,

        state: AgentState

    ):

        self.log(
            "Received Query"
        )

        self.log(

            f"User ID: {state.user_id}"

        )

        self.log(

            f"Email: {state.email}"

        )

        result = (
            self.detector.detect(
                state.user_query
            )
        )

        state.domain = (
            result["domain"]
        )

        self.log(
            f"Detected Domain: {state.domain}"
        )

        state = (
            self.planner.execute(
                state
            )
        )

        agent = (
            self.registry.get_agent(
                state.domain
            )
        )

        if agent:

            self.log(

                f"Executing Agent: {agent.__class__.__name__}"

            )

            import inspect
            if inspect.iscoroutinefunction(agent.execute):
                state = (
                    await agent.execute(
                        state
                    )
                )
            else:
                state = (
                    agent.execute(
                        state
                    )
                )

        else:

            self.log(

                f"No Agent Found For Domain: {state.domain}"

            )

        # --------------------------------------------------
        # Memory Layer (RAG + LLM)
        # --------------------------------------------------

        if not getattr(state, "response", None):

            state = (

                self.memory.execute(

                    state

                )

            )
        # --------------------------------------------------
        # Response Synthesis (Phase 17)
        # --------------------------------------------------
        if not getattr(state, "response", None) and not getattr(state, "final_response", None):
            self.log("Synthesizing response using LLM (Phase 17)")
            prompt = f"""
You are the assistant for the Universal Problem Solving System (UPSS).
Answer the user's query utilizing the retrieved memory context (facts, conversation history, episodic milestones, and tool outputs) if available.

Retrieved Memory Context:
{state.memory_context or "No past profile facts stored yet."}

User Query:
{state.user_query}

CRITICAL INSTRUCTION:
If the "Retrieved Memory Context" contains "Retrieved General Task Execution Output" or tool results (like weather data, calculator results, or distances), you MUST use this information to answer the user's query directly. Do NOT apologize or claim you do not have access to real-time data, because the tools have successfully retrieved this real-time data for you.

Respond naturally and directly. If the user's name or nickname is available in the retrieved memory context, ALWAYS personalize your greeting by addressing them with their name (e.g. "Hello Tara!" or "Hi Vansh!") so they know you remember them. Reference other facts or past milestones naturally.
"""
            from llm.router.model_router import ModelRouter
            llm = ModelRouter()
            state.response = llm.generate(
                prompt=prompt,
                query=state.user_query,
                domain=state.domain or "general"
            )

        # --------------------------------------------------
        # Reporting Layer
        # --------------------------------------------------
        state = (

            self.reporter.execute(

                state

            )

        )

        return (

            state

        )