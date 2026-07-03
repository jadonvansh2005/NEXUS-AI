from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState
from agents.workflow.workflow_agent import WorkflowAgent

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResearchAgent")
        self.workflow_agent = WorkflowAgent()

    async def execute(self, state: AgentState) -> AgentState:
        self.log(f"Executing Research Workflow for Query: {state.user_query}")
        
        # 1. Run the workflow tasks decomposed by the planner (e.g. read_webpage / search)
        state = await self.workflow_agent.execute(state)
        
        # 2. Extract the results of the executed tasks
        results = getattr(state.workflow_state, "results", {})
        task_output = None
        for task_id, output in results.items():
            if output:
                task_output = output
                break
                
        # 3. Format and store task output in memory_context for LLM response synthesis
        formatted_output = ""
        if task_output:
            if isinstance(task_output, dict):
                # If it's a search response with a results list
                if "results" in task_output:
                    formatted_results = []
                    for item in task_output["results"]:
                        title = item.get("title", "")
                        url = item.get("url", "")
                        snippet = item.get("snippet", "")
                        formatted_results.append(f"- **[{title}]({url})**\n  {snippet}")
                    formatted_output = "\n\n".join(formatted_results)
                # If it's a webpage reader response with page content
                elif "page" in task_output and task_output["page"]:
                    page_data = task_output["page"]
                    formatted_output = page_data.get("markdown", "") or page_data.get("text", "")
                else:
                    formatted_output = str(task_output)
            else:
                formatted_output = str(task_output)
        else:
            formatted_output = "Could not retrieve any research results."
            
        # Store in memory_context and keep response None so LLM synthesis triggers
        state.memory_context = (state.memory_context or "") + f"\n\nRetrieved Web Search & Article Data:\n{formatted_output}"
        state.response = None
            
        return state
