"""
UPSS SQL Backup Tool

Creates PostgreSQL database backups using pg_dump.
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from app.settings import settings

from tools.base_tool import BaseTool
from tools.tool_context import ToolContext
from tools.tool_permission import ToolPermission
from tools.tool_result import ToolResult
from tools.tool_schema import (
    ToolCategory,
    ToolMetadata,
)


class BackupTool(BaseTool):
    """
    Create PostgreSQL database backup using pg_dump.
    """

    metadata = ToolMetadata(
        name="sql.backup",
        display_name="Database Backup",
        description="Create PostgreSQL database backup.",
        category=ToolCategory.DATABASE,
        tags=[
            "sql",
            "postgresql",
            "backup",
        ],
    )

    permission = ToolPermission.requires_confirmation()

    async def execute(
        self,
        context: ToolContext,
        request: dict | None = None,
    ) -> ToolResult:

        request = request or {}

        # --------------------------------------------------
        # Parse DATABASE_URL
        # --------------------------------------------------

        parsed = urlparse(settings.DATABASE_URL)

        host = parsed.hostname or "localhost"

        port = str(parsed.port or 5432)

        username = parsed.username or "postgres"

        database = parsed.path.lstrip("/")

        password = parsed.password

        # --------------------------------------------------
        # PostgreSQL Binary
        # --------------------------------------------------

        postgres_bin = getattr(
            settings,
            "POSTGRES_BIN",
            None,
        )

        if postgres_bin:

            pg_dump = (
                Path(postgres_bin)
                / "pg_dump.exe"
            )

        else:

            pg_dump = Path("pg_dump")

        # --------------------------------------------------
        # Validate pg_dump
        # --------------------------------------------------

        if postgres_bin and not pg_dump.exists():

            return ToolResult.failure(

                message=f"pg_dump not found at {pg_dump}",

            )

        # --------------------------------------------------
        # Backup Directory
        # --------------------------------------------------

        backup_directory = Path(

            request.get(
                "backup_directory",
                "backups",
            )

        )

        backup_directory.mkdir(

            parents=True,

            exist_ok=True,

        )

        backup_file = (

            backup_directory

            / f"{datetime.now():%Y%m%d_%H%M%S}.sql"

        )

        # --------------------------------------------------
        # Environment
        # --------------------------------------------------

        env = os.environ.copy()

        if password:

            env["PGPASSWORD"] = password

        # --------------------------------------------------
        # Command
        # --------------------------------------------------

        command = [

            str(pg_dump),

            "-h",
            host,

            "-p",
            port,

            "-U",
            username,

            "-d",
            database,

            "-F",
            "p",

            "-f",
            str(backup_file),

        ]

        # --------------------------------------------------
        # Execute
        # --------------------------------------------------

        process = await asyncio.create_subprocess_exec(

            *command,

            stdout=asyncio.subprocess.PIPE,

            stderr=asyncio.subprocess.PIPE,

            env=env,

        )

        stdout, stderr = await process.communicate()

        # --------------------------------------------------
        # Failure
        # --------------------------------------------------

        if process.returncode != 0:

            return ToolResult.failure(

                message="Database backup failed.",

                data={

                    "command": " ".join(command),

                    "stdout": stdout.decode(

                        "utf-8",

                        errors="replace",

                    ),

                    "stderr": stderr.decode(

                        "utf-8",

                        errors="replace",

                    ),

                },

            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        return ToolResult.ok(

            message="Database backup completed successfully.",

            data={

                "backup_file": str(
                    backup_file.resolve()
                ),

                "database": database,

                "host": host,

                "port": port,

                "command": " ".join(command),

            },

        )