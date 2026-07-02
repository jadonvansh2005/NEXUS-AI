"""
UPSS Execute SQL Tool

Executes SQL statements using the project's
existing SQLAlchemy Session.
"""

from __future__ import annotations

import time

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
    SQLExecuteRequest,
    SQLResponse,
)


class ExecuteSQLTool(BaseTool):
    """
    Execute SQL statements.

    Supports:

    - SELECT
    - INSERT
    - UPDATE
    - DELETE
    - CREATE
    - ALTER
    - DROP
    """

    metadata = ToolMetadata(

        name="sql.execute",

        display_name="SQL Executor",

        description="Execute SQL statements.",

        category=ToolCategory.DATABASE,

        tags=[
            "sql",
            "database",
            "postgresql",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    input_model = SQLExecuteRequest

    async def execute(
        self,
        context: ToolContext,
        request: SQLExecuteRequest,
    ) -> ToolResult:

        db = SessionLocal()

        start = time.perf_counter()

        try:

            result = db.execute(
                text(request.statement)
            )

            db.commit()

            execution_time = (
                time.perf_counter() - start
            )

            rows = []

            try:

                rows = [
                    dict(row._mapping)
                    for row in result
                ]

            except Exception:
                pass

            response = SQLResponse(

                success=True,

                rows=rows,

                affected_rows=result.rowcount,

                execution_time=execution_time,

                message="SQL executed successfully.",

            )

            return ToolResult.ok(

                message=response.message,

                data=response.model_dump(),

            )

        except Exception as exc:

            db.rollback()

            response = SQLResponse(

                success=False,

                rows=[],

                affected_rows=0,

                execution_time=0.0,

                message=str(exc),

            )

            return ToolResult.failure(

                message=str(exc),

                data=response.model_dump(),

            )

        finally:

            db.close()