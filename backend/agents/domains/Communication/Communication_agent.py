from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState
from agents.workflow.workflow_agent import WorkflowAgent

class CommunicationAgent(BaseAgent):
    def __init__(self):
        super().__init__("CommunicationAgent")
        self.workflow_agent = WorkflowAgent()

    async def execute(self, state: AgentState) -> AgentState:
        self.log(f"Executing Communication Agent for Query: {state.user_query}")
        
        # 1. Run the workflow tasks decomposed by the planner (e.g. email tools)
        self.log("Initiating communication tools workflow.")
        state = await self.workflow_agent.execute(state)
        
        # 2. Extract the results of the executed tasks
        results = getattr(state.workflow_state, "results", {})
        task_outputs = []
        for task_id, output in results.items():
            if output:
                # Format each task result nicely
                task_outputs.append(f"### Task {task_id} Result:\n{output}")
                
        # 3. Format and store task output in memory_context for LLM response synthesis
        formatted_output = "\n\n".join(task_outputs) if task_outputs else "Could not perform communication task execution."
            
        # Store in memory_context and keep response None so LLM synthesis triggers
        state.memory_context = (state.memory_context or "") + f"\n\nRetrieved Communication Task Execution Output:\n{formatted_output}"
        state.response = None
            
        return state
