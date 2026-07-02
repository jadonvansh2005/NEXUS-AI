"""
UPSS Currency Converter Tool

Convert between currencies.

Current:
    Returns a normalized conversion request.

Future providers:

- ExchangeRate.host
- Open Exchange Rates
- Fixer.io
- CurrencyAPI
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
    CurrencyConverterRequest,
    TravelResponse,
)


class CurrencyConverterTool(BaseTool):
    """
    Convert between currencies.
    """

    metadata = ToolMetadata(

        name="travel.currency_converter",

        display_name="Currency Converter",

        description="Convert between currencies.",

        category=ToolCategory.TRAVEL,

        tags=[
            "travel",
            "currency",
            "exchange",
            "finance",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = CurrencyConverterRequest

    async def execute(
        self,
        context: ToolContext,
        request: CurrencyConverterRequest,
    ) -> ToolResult:

        #
        # Future Provider Integration
        #
        # provider = ProviderFactory.get(...)
        #
        # conversion = await provider.convert(
        #     amount=request.amount,
        #     from_currency=request.from_currency,
        #     to_currency=request.to_currency,
        # )
        #

        conversion = {

            "amount": request.amount,

            "from_currency": request.from_currency.upper(),

            "to_currency": request.to_currency.upper(),

            "status": "conversion_pending",

            "provider": "future_provider",

        }

        response = TravelResponse(

            success=True,

            message="Currency conversion request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "conversion": conversion,

                **response.model_dump(),

            },

        )