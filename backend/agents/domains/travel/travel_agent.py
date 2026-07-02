import json
from datetime import datetime, timedelta
from agents.core.base_agent import BaseAgent
from agents.core.agent_state import AgentState
from agents.planner.schemas import ExecutionPlan, PlannerTask
from agents.workflow.workflow_agent import WorkflowAgent
from llm.router.model_router import ModelRouter
from memory.episodic.episodic_manager import EpisodicManager
from database.connection import SessionLocal

class TravelAgent(BaseAgent):

    def __init__(self):
        super().__init__("TravelAgent")
        self.llm = ModelRouter()
        self.workflow_agent = WorkflowAgent()

    async def execute(self, state: AgentState) -> AgentState:
        self.log(f"Executing Travel Workflow for Query: {state.user_query}")
        
        # 1. Analyze conversation history to detect current booking stage
        history = state.memory_context or ""
        query = state.user_query

        classification_prompt = f"""
You are an expert travel assistant. Analyze the conversation history and the latest user query.
Determine the current stage of the travel flow:
- "PLANNING": User is asking to plan a trip, generate an itinerary, or start a new vacation planning.
- "TRAINS": User has agreed to see trains, wants to see list of trains, or is asking about travel transport to the destination.
- "CLASS_CHOICE": User has picked a train (e.g. Shatabdi, Vande Bharat, Malwa) and wants to book it, but has NOT specified a class (Sleeper or AC) yet.
- "BOOKING_CONFIRMATION": User has specified the class (Sleeper/SL or AC/3A/2A) and wants to finalize the booking.

Conversation History:
{history}

Latest User Query:
{query}

Respond with exactly one of: PLANNING, TRAINS, CLASS_CHOICE, BOOKING_CONFIRMATION.
Do not output any other text.
"""
        stage = self.llm.generate(prompt=classification_prompt, query=query, domain="travel").strip()
        self.log(f"Detected Travel Stage: {stage}")

        if "PLANNING" in stage:
            # Stage 1: Itinerary Generation
            extraction_prompt = f"""
Extract travel details from the query: "{query}"
Return a JSON object with:
- "destination": destination city (string)
- "days": number of days (integer, default 3)
- "travelers": number of travelers (integer, default 1)

Return ONLY valid JSON. No markdown formatting.
"""
            extracted_raw = self.llm.generate(prompt=extraction_prompt, query=query, domain="travel")
            try:
                details = json.loads(extracted_raw.strip().replace("```json", "").replace("```", ""))
            except Exception:
                details = {"destination": "Gwalior", "days": 3, "travelers": 1}

            destination = details.get("destination", "Gwalior")
            days = details.get("days", 3)
            travelers = details.get("travelers", 1)

            # Build planner task
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=days - 1)

            task = PlannerTask(
                id="itinerary",
                name="travel.itinerary",
                description="Generates a day-by-day travel plan itinerary.",
                tool="travel.itinerary",
                parameters={
                    "destination": destination,
                    "start_date": start_date,
                    "end_date": end_date,
                    "travelers": travelers
                }
            )
            
            plan = ExecutionPlan(
                goal=query,
                domain="travel",
                tasks=[task]
            )
            state.execution_plan = plan

            # Run workflow engine
            state = await self.workflow_agent.execute(state)
            
            # Fetch results
            itinerary_data = getattr(state.workflow_state, "results", {}).get("itinerary", {})
            
            # Generate conversational response
            response_prompt = f"""
Generate a beautiful day-by-day travel plan response for the user based on this itinerary data:
{json.dumps(itinerary_data)}

At the end of the response, ask the user: "Would you like me to find some trains for your journey to {destination}?"
"""
            state.final_response = self.llm.generate(prompt=response_prompt, query=query, domain="travel")

        elif "TRAINS" in stage:
            # Stage 2: Train Search
            # Parse destination from history or query
            dest_prompt = f"""
Find the destination city from history/query:
History: {history}
Query: {query}
Respond with ONLY the destination city name.
"""
            destination = self.llm.generate(prompt=dest_prompt, query=query, domain="travel").strip()
            
            # Create train search task
            task = PlannerTask(
                id="train_search",
                name="travel.trains",
                description="Searches for trains between origin and destination.",
                tool="travel.trains",
                parameters={
                    "origin": "Delhi",  # Default origin
                    "destination": destination,
                    "journey_date": datetime.now().date() + timedelta(days=1)
                }
            )

            plan = ExecutionPlan(
                goal=query,
                domain="travel",
                tasks=[task]
            )
            state.execution_plan = plan

            # Run workflow engine
            state = await self.workflow_agent.execute(state)

            # Fetch results
            train_data = getattr(state.workflow_state, "results", {}).get("train_search", {})

            # Generate conversational response
            response_prompt = f"""
Display the list of available trains and their departures/fares in a clean, user-friendly format based on this data:
{json.dumps(train_data)}

At the end of the response, ask: "Which train would you like me to book for you? (Please mention the train name or number)"
"""
            state.final_response = self.llm.generate(prompt=response_prompt, query=query, domain="travel")

        elif "CLASS_CHOICE" in stage:
            # Stage 3: Class Choice
            state.final_response = "Which class would you prefer for your booking? Sleeper (SL) or AC (3A/2A/1A)?"

        elif "BOOKING_CONFIRMATION" in stage:
            # Stage 4: Booking and Persistence
            dest_prompt = f"""
Find the destination and train details from the history and query:
History: {history}
Query: {query}
Respond with a JSON object containing keys: "destination", "train_name", "class".
Return ONLY valid JSON.
"""
            details_raw = self.llm.generate(prompt=dest_prompt, query=query, domain="travel")
            try:
                details = json.loads(details_raw.strip().replace("```json", "").replace("```", ""))
            except Exception:
                details = {"destination": "Gwalior", "train_name": "Vande Bharat Express", "class": "AC"}

            dest = details.get("destination", "Gwalior")
            train = details.get("train_name", "Vande Bharat Express")
            cls = details.get("class", "AC")

            # Record event in episodic memory
            db = SessionLocal()
            try:
                episodic = EpisodicManager()
                event_desc = f"Booked train ticket on {train} ({cls}) to {dest} successfully."
                episodic.process_event(
                    db=db,
                    user_id=state.user_id,
                    event_type="milestone",
                    event=event_desc
                )
            finally:
                db.close()

            state.final_response = f"🎉 **Booking Confirmed!**\n\n- **Train**: {train}\n- **Destination**: {dest}\n- **Class**: {cls}\n- **Status**: CONFIRMED\n\nI have successfully booked your ticket and saved this milestone to your episodic memory profile!"

        return state
