import asyncio
from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import ToolCategory, ToolMetadata
from tools.travel.schemas import FlightSearchRequest

class FlightSearchTool(BaseTool):
    metadata = ToolMetadata(
        name="travel.flights",
        display_name="Flight Search",
        description="Searches for flights between origin and destination.",
        category=ToolCategory.TRAVEL,
        tags=["travel", "flight", "search"],
    )

    permission = ToolPermission.read_only()
    input_model = FlightSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: FlightSearchRequest,
    ) -> ToolResult:
        origin = request.origin
        destination = request.destination
        
        flights = [
            {
                "flight_no": "6E-502",
                "airline": "IndiGo",
                "departure": "07:15",
                "arrival": "08:45",
                "price": 4200
            },
            {
                "flight_no": "AI-809",
                "airline": "Air India",
                "departure": "12:30",
                "arrival": "14:15",
                "price": 5100
            }
        ]

        return ToolResult.ok(
            message=f"Found 2 flights running from {origin} to {destination}.",
            data={
                "origin": origin,
                "destination": destination,
                "flights": flights
            }
        )