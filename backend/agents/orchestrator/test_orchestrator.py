from agents.core.agent_state import AgentState

from agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent
)

state = AgentState(
    user_query=
    "i have a dataset i want to analyze. can you help me with that?"
)

agent = (
    OrchestratorAgent()
)

result = (
    agent.execute(state)
)

print("\nDomain:")
print(result.domain)

print("\nPlan:")
for task in result.execution_plan:
    print("-", task)

print("\nResponse:")
print(result.final_response)