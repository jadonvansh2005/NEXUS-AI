"""
UPSS Invoice Generator Tool

Generate invoices.

Future integrations:

- Report Module
- PDF Generator
- DOCX Generator
- HTML Generator
- Financial Report Tool
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

from tools.finance.schemas import (
    InvoiceGeneratorRequest,
    FinanceResponse,
)


class InvoiceGeneratorTool(BaseTool):
    """
    Generate invoices.
    """

    metadata = ToolMetadata(

        name="finance.invoice_generator",

        display_name="Invoice Generator",

        description="Generate professional invoices.",

        category=ToolCategory.FINANCE,

        tags=[
            "finance",
            "invoice",
            "billing",
            "report",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = InvoiceGeneratorRequest

    async def execute(
        self,
        context: ToolContext,
        request: InvoiceGeneratorRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # InvoiceBuilder.build(...)
        #
        # ReportModule.generate(
        #     format="pdf",
        # )
        #
        # PDFGenerator(...)
        #
        # DOCXGenerator(...)
        #
        # HTMLGenerator(...)
        #
        # FinancialReportTool.execute(...)
        #

        result = {

            "client_name":

                request.client_name,

            "currency":

                request.currency,

            "item_count":

                len(request.items),

            "status":

                "invoice_generation_pending",

            "message": (

                "Invoice generation will "

                "be performed after "

                "Report module "

                "integration."

            ),

        }

        response = FinanceResponse(

            success=True,

            message="Invoice generation request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "invoice": result,

                **response.model_dump(),

            },

        )