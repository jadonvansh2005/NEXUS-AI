import asyncio
from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import ToolCategory, ToolMetadata
from tools.travel.schemas import TrainSearchRequest

class TrainSearchTool(BaseTool):
    metadata = ToolMetadata(
        name="travel.trains",
        display_name="Train Search",
        description="Searches for trains between origin and destination.",
        category=ToolCategory.TRAVEL,
        tags=["travel", "train", "search"],
    )

    permission = ToolPermission.read_only()
    input_model = TrainSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: TrainSearchRequest,
    ) -> ToolResult:
        origin = request.origin
        destination = request.destination
        
        # Mock trains list
        trains = [
            {
                "train_no": "12002",
                "train_name": "Shatabdi Express",
                "departure": "06:00",
                "arrival": "10:30",
                "duration": "4h 30m",
                "fares": {"SL": 380, "CC": 720, "EC": 1450}
            },
            {
                "train_no": "22416",
                "train_name": "Vande Bharat Express",
                "departure": "08:15",
                "arrival": "11:45",
                "duration": "3h 30m",
                "fares": {"CC": 950, "EC": 1880}
            },
            {
                "train_no": "12920",
                "train_name": "Malwa Express",
                "departure": "13:40",
                "arrival": "19:10",
                "duration": "5h 30m",
                "fares": {"SL": 290, "3A": 780, "2A": 1100, "1A": 1850}
            }
        ]

        return ToolResult.ok(
            message=f"Found 3 trains running from {origin} to {destination}.",
            data={
                "origin": origin,
                "destination": destination,
                "journey_date": str(request.journey_date),
                "trains": trains
            }
        )