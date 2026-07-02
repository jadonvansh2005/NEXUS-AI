import asyncio
from datetime import datetime
from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import ToolCategory, ToolMetadata
from tools.travel.schemas import ItineraryRequest

class ItineraryTool(BaseTool):
    metadata = ToolMetadata(
        name="travel.itinerary",
        display_name="Itinerary Generator",
        description="Generates a day-by-day travel plan itinerary.",
        category=ToolCategory.TRAVEL,
        tags=["travel", "itinerary", "plan"],
    )

    permission = ToolPermission.read_only()
    input_model = ItineraryRequest

    async def execute(
        self,
        context: ToolContext,
        request: ItineraryRequest,
    ) -> ToolResult:
        destination = request.destination
        travelers = request.travelers
        budget = request.budget
        
        # Calculate days
        delta = request.end_date - request.start_date
        days = max(1, delta.days + 1)

        itinerary = {}
        for day in range(1, days + 1):
            itinerary[f"Day {day}"] = [
                f"Morning: Visit top sightseeing spots in {destination}.",
                f"Afternoon: Lunch at local restaurants, walk around the city center.",
                f"Evening: Leisure activity and dinner."
            ]

        return ToolResult.ok(
            message=f"Generated a {days}-day itinerary for {destination}.",
            data={
                "destination": destination,
                "days": days,
                "travelers": travelers,
                "budget": budget,
                "itinerary": itinerary
            }
        )