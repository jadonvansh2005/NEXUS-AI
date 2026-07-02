"""
UPSS SQL Runner Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DatabaseType(str, Enum):

    POSTGRESQL = "postgresql"

    MYSQL = "mysql"

    SQLITE = "sqlite"

    MSSQL = "mssql"


class SQLQueryRequest(BaseModel):
    """
    Execute a read-only SQL query.
    """

    query: str = Field(
        ...,
        description="SQL query.",
    )

    database: DatabaseType = DatabaseType.POSTGRESQL

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
    )


class SQLExecuteRequest(BaseModel):
    """
    Execute INSERT/UPDATE/DELETE/DDL statements.
    """

    statement: str = Field(
        ...,
        description="SQL statement.",
    )

    database: DatabaseType = DatabaseType.POSTGRESQL

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
    )


class SQLTransactionRequest(BaseModel):
    """
    Execute multiple SQL statements atomically.
    """

    statements: list[str]

    database: DatabaseType = DatabaseType.POSTGRESQL

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
    )


class SQLResponse(BaseModel):

    success: bool

    rows: list[dict] = Field(
        default_factory=list,
    )

    affected_rows: int = 0

    execution_time: float = 0.0

    message: str = ""