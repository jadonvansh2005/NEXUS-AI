"""
UPSS Schema Tool

Reads database schema information.
"""

from __future__ import annotations

import time

from sqlalchemy import inspect

from database.connection import engine

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)


class SchemaTool(BaseTool):
    """
    Read database schema.

    Returns

    - Tables
    - Columns
    - Primary Keys
    - Foreign Keys
    """

    metadata = ToolMetadata(

        name="sql.schema",

        display_name="Database Schema",

        description="Read database schema.",

        category=ToolCategory.DATABASE,

        tags=[
            "sql",
            "schema",
            "database",
        ],
    )

    permission = ToolPermission.read_only()

    async def execute(
        self,
        context: ToolContext,
        request=None,
    ) -> ToolResult:

        start = time.perf_counter()

        try:

            inspector = inspect(engine)

            schema = []

            for table in inspector.get_table_names():

                columns = []

                for column in inspector.get_columns(table):

                    columns.append(

                        {
                            "name": column["name"],
                            "type": str(column["type"]),
                            "nullable": column["nullable"],
                            "default": str(
                                column.get("default")
                            ),
                        }

                    )

                schema.append(

                    {
                        "table": table,
                        "columns": columns,
                        "primary_key": inspector.get_pk_constraint(
                            table
                        ),
                        "foreign_keys": inspector.get_foreign_keys(
                            table
                        ),
                    }

                )

            return ToolResult.ok(

                message="Schema loaded successfully.",

                data={

                    "execution_time": (
                        time.perf_counter() - start
                    ),

                    "tables": schema,

                },

            )

        except Exception as exc:

            return ToolResult.failure(

                message=str(exc),

            )