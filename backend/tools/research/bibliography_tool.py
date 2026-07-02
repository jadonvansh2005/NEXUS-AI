"""
UPSS Bibliography Tool

Generate formatted bibliographies.

Future integrations:

- Citation Generator Tool
- CSL Processor
- Crossref
- DOI Resolver
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

from tools.research.schemas import (
    BibliographyRequest,
    ResearchResponse,
)


class BibliographyTool(BaseTool):
    """
    Generate formatted bibliographies.
    """

    metadata = ToolMetadata(

        name="research.bibliography",

        display_name="Bibliography Generator",

        description="Generate formatted bibliographies from citations.",

        category=ToolCategory.RESEARCH,

        tags=[
            "research",
            "bibliography",
            "references",
            "citations",
        ],

    )

    permission = ToolPermission.read_only()

    input_model = BibliographyRequest

    async def execute(
        self,
        context: ToolContext,
        request: BibliographyRequest,
    ) -> ToolResult:

        #
        # Future Pipeline
        #
        # validated = CitationValidator.validate(
        #     request.citations,
        # )
        #
        # bibliography = CitationFormatter.generate_bibliography(
        #     citations=validated,
        #     style=request.style,
        # )
        #
        # CSLProcessor.format(...)
        #
        # Crossref.complete_missing_metadata(...)
        #

        result = {

            "citation_count": len(
                request.citations
            ),

            "style": request.style,

            "status": "bibliography_generation_pending",

            "message": (

                "Bibliography generation "

                "will be performed after "

                "citation engine integration."

            ),

        }

        response = ResearchResponse(

            success=True,

            message="Bibliography request prepared successfully.",

        )

        return ToolResult.ok(

            message=response.message,

            data={

                "bibliography": result,

                **response.model_dump(),

            },

        )