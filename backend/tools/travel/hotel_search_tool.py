import asyncio
from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import ToolCategory, ToolMetadata
from tools.travel.schemas import HotelSearchRequest

class HotelSearchTool(BaseTool):
    metadata = ToolMetadata(
        name="travel.hotels",
        display_name="Hotel Search",
        description="Searches for hotels at the destination.",
        category=ToolCategory.TRAVEL,
        tags=["travel", "hotel", "search"],
    )

    permission = ToolPermission.read_only()
    input_model = HotelSearchRequest

    async def execute(
        self,
        context: ToolContext,
        request: HotelSearchRequest,
    ) -> ToolResult:
        destination = request.destination
        
        hotels = [
            {
                "hotel_name": "Hotel Taj Mahal Palace",
                "rating": "4.8",
                "price_per_night": 7500,
                "amenities": ["Wifi", "AC", "Pool", "Breakfast"]
            },
            {
                "hotel_name": "Grand Regency Palace",
                "rating": "4.2",
                "price_per_night": 3800,
                "amenities": ["Wifi", "AC", "Breakfast"]
            },
            {
                "hotel_name": "Comfort Residency",
                "rating": "3.9",
                "price_per_night": 2200,
                "amenities": ["Wifi", "AC"]
            }
        ]

        return ToolResult.ok(
            message=f"Found 3 hotels matching criteria in {destination}.",
            data={
                "destination": destination,
                "hotels": hotels
            }
        )