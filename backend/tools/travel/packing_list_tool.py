"""
UPSS Packing List Tool

Generate a travel packing checklist based on:

- Destination
- Duration
- Weather
- Activities
"""

from __future__ import annotations

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.travel.schemas import (
    PackingListRequest,
    TravelResponse,
)


class PackingListTool(BaseTool):
    """
    Generate a travel packing checklist.
    """

    metadata = ToolMetadata(

        name="travel.packing_list",

        display_name="Packing List",

        description="Generate a personalized travel packing checklist.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "packing",
            "checklist",
            "luggage",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = PackingListRequest

    async def execute(
        self,
        context: ToolContext,
        request: PackingListRequest,
    ) -> ToolResult:

        items = [

            "Passport / ID",

            "Travel Tickets",

            "Wallet",

            "Phone Charger",

            "Power Bank",

            "Toiletries",

            "Medicines",

        ]

        #
        # Duration
        #

        if request.days >= 3:

            items.extend(

                [

                    "Extra Clothes",

                    "Laundry Bag",

                ]

            )

        if request.days >= 7:

            items.extend(

                [

                    "Travel Pillow",

                    "Extra Footwear",

                ]

            )

        #
        # Weather
        #

        weather = request.weather.lower()

        if "cold" in weather:

            items.extend(

                [

                    "Jacket",

                    "Sweater",

                    "Gloves",

                    "Thermal Wear",

                ]

            )

        elif "hot" in weather:

            items.extend(

                [

                    "Sunglasses",

                    "Cap",

                    "Sunscreen",

                ]

            )

        elif "rain" in weather:

            items.extend(

                [

                    "Umbrella",

                    "Raincoat",

                    "Waterproof Shoes",

                ]

            )

        #
        # Activities
        #

        activities = {

            activity.lower()

            for activity in request.activities

        }

        if "beach" in activities:

            items.extend(

                [

                    "Swimwear",

                    "Flip-flops",

                    "Beach Towel",

                ]

            )

        if "hiking" in activities:

            items.extend(

                [

                    "Hiking Shoes",

                    "Water Bottle",

                    "Backpack",

                ]

            )

        if "business" in activities:

            items.extend(

                [

                    "Formal Clothes",

                    "Laptop",

                    "Business Cards",

                ]

            )

        if "camping" in activities:

            items.extend(

                [

                    "Flashlight",

                    "Sleeping Bag",

                    "First Aid Kit",

                ]

            )

        #
        # Remove duplicates
        #

        items = sorted(

            set(items)

        )

        response = TravelResponse(

            success=True,

            message="Packing list generated successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "destination": request.destination,

                "days": request.days,

                "weather": request.weather,

                "activities": request.activities,

                "total_items": len(items),

                "packing_list": items,

                **response.model_dump(),

            },

        )