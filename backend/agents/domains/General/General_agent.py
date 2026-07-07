from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState
from agents.workflow.workflow_agent import WorkflowAgent

class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("GeneralAgent")
        self.workflow_agent = WorkflowAgent()

    async def execute(self, state: AgentState) -> AgentState:
        self.log(f"Executing General Agent for Query: {state.user_query}")
        
        # 1. Check if query contains keywords for weather, maps, or calculator tools
        query = state.user_query.lower()
        has_tool_keywords = any(
            w in query
            for w in [
                "weather", "temp", "temperature", "rain", "forecast", "cloudy", "wind", "climate",
                "aqi", "air quality", "pollution", "alert", "alerts", "warning", "warnings",
                "map", "distance", "route", "navigate", "location", "places", "nearby", "geocode",
                "coordinates", "directions", "direction", "address",
                "calculate", "calculator", "math", "+", "-", "*", "/", "sum", "add", "multiply", "divide",
                "screenshot", "screen capture", "capture webpage", "capture page", "download", "browser history", "browser search"
            ]
        )
        
        if not has_tool_keywords:
            # Simple conversational query: bypass workflow completely to prevent active tools
            self.log("Conversational query detected (no weather/maps/calculator keywords). Bypassing workflow.")
            state.response = None
            return state

        # 2. Run the workflow tasks decomposed by the planner (e.g. weather, calculation, maps tools)
        self.log("Tool keywords detected. Initiating tools workflow.")
        state = await self.workflow_agent.execute(state)
        
        # 3. Extract the results of the executed tasks
        results = getattr(state.workflow_state, "results", {})
        task_outputs = []
        for task_id, output in results.items():
            if output:
                # Format each task result nicely
                task_outputs.append(f"### Task {task_id} Result:\n{output}")
                
        # 4. Format and store task output in memory_context for LLM response synthesis
        formatted_output = "\n\n".join(task_outputs) if task_outputs else "Could not perform general task execution."
            
        # Store in memory_context and keep response None so LLM synthesis triggers
        state.memory_context = (state.memory_context or "") + f"\n\nRetrieved General Task Execution Output:\n{formatted_output}"
        print(f"[DIAGNOSTIC] GeneralAgent memory_context populated:\n{state.memory_context}")
        state.response = None
            
        return state
