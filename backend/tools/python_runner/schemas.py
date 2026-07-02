"""
UPSS Python Runner Schemas
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


# ==========================================================
# Python Code Execution
# ==========================================================

class PythonExecutionRequest(BaseModel):
    """
    Execute Python source code.
    """

    code: str = Field(
        ...,
        description="Python source code.",
    )

    timeout: int = Field(
        default=300,
        ge=1,
        le=3600,
    )

    working_directory: str | None = None


class PythonExecutionResponse(BaseModel):
    """
    Response after Python execution.
    """

    success: bool

    stdout: str

    stderr: str

    execution_time: float

    globals: dict = Field(
        default_factory=dict,
    )


# ==========================================================
# Package Installation
# ==========================================================

class PackageInstallRequest(BaseModel):
    """
    Install one or more Python packages.
    """

    packages: list[str] = Field(
        ...,
        description="Packages to install.",
    )

    timeout: int = Field(
        default=600,
        ge=1,
        le=3600,
    )

    working_directory: str | None = None


class PackageInstallResponse(BaseModel):
    """
    Response after package installation.
    """

    success: bool

    installed_packages: list[str]

    stdout: str

    stderr: str

    exit_code: int


# ==========================================================
# Notebook Execution
# ==========================================================

class NotebookExecutionRequest(BaseModel):
    """
    Execute a Jupyter notebook.
    """

    path: Path

    timeout: int = Field(
        default=600,
        ge=1,
        le=7200,
    )


class NotebookExecutionResponse(BaseModel):
    """
    Response after notebook execution.
    """

    success: bool

    executed_notebook: str

    outputs: list[str] = Field(
        default_factory=list,
    )

    error: str | None = None