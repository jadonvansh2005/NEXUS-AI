"""
UPSS SQL Export Tool

Executes a SQL query and exports the results.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

from openpyxl import Workbook
from sqlalchemy import text

from database.connection import SessionLocal

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)

from tools.sql_runner.schemas import (
    SQLQueryRequest,
)


class ExportTool(BaseTool):
    """
    Execute a SELECT query and export
    the result to CSV / Excel / JSON.
    """

    metadata = ToolMetadata(

        name="sql.export",

        display_name="SQL Export",

        description="Export SQL query results.",

        category=ToolCategory.DATABASE,

        tags=[
            "sql",
            "database",
            "export",
        ],
    )

    permission = ToolPermission.read_only()

    input_model = SQLQueryRequest

    async def execute(
        self,
        context: ToolContext,
        request: SQLQueryRequest,
    ) -> ToolResult:

        export_format = getattr(
            request,
            "export_format",
            "csv",
        ).lower()

        output_path = Path(
            getattr(
                request,
                "output_path",
                f"export.{export_format}",
            )
        )

        db = SessionLocal()

        try:

            result = db.execute(
                text(request.query)
            )

            rows = [
                dict(row._mapping)
                for row in result
            ]

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            # ------------------------
            # CSV
            # ------------------------

            if export_format == "csv":

                with output_path.open(
                    "w",
                    newline="",
                    encoding="utf-8",
                ) as file:

                    writer = csv.DictWriter(
                        file,
                        fieldnames=rows[0].keys()
                        if rows
                        else [],
                    )

                    writer.writeheader()

                    writer.writerows(rows)

            # ------------------------
            # JSON
            # ------------------------

            elif export_format == "json":

                output_path.write_text(

                    json.dumps(
                        rows,
                        indent=2,
                        default=str,
                    ),

                    encoding="utf-8",

                )

            # ------------------------
            # Excel
            # ------------------------

            elif export_format == "xlsx":

                workbook = Workbook()

                sheet = workbook.active

                if rows:

                    sheet.append(
                        list(rows[0].keys())
                    )

                    for row in rows:

                        sheet.append(
                            list(row.values())
                        )

                workbook.save(
                    output_path
                )

            else:

                return ToolResult.failure(

                    message=f"Unsupported export format: {export_format}"

                )

            return ToolResult.ok(

                message="Export completed successfully.",

                data={

                    "rows": len(rows),

                    "file": str(
                        output_path.resolve()
                    ),

                    "format": export_format,

                },

            )

        except Exception as exc:

            return ToolResult.failure(

                message=str(exc),

            )

        finally:

            db.close()