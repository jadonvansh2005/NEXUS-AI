"""
UPSS Coding Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class CodingProvider(str, Enum):

    GENERIC = "generic"

    GITHUB = "github"

    GITLAB = "gitlab"

    BITBUCKET = "bitbucket"


# ==========================================================
# Project Generator
# ==========================================================

class ProjectGeneratorRequest(BaseModel):

    project_name: str

    description: str

    language: str

    framework: str | None = None


# ==========================================================
# Code Generator
# ==========================================================

class CodeGeneratorRequest(BaseModel):

    prompt: str

    language: str

    framework: str | None = None


# ==========================================================
# Code Reviewer
# ==========================================================

class CodeReviewRequest(BaseModel):

    code: str

    language: str


# ==========================================================
# Bug Fixer
# ==========================================================

class BugFixRequest(BaseModel):

    code: str

    language: str

    error_message: str


# ==========================================================
# Debugger
# ==========================================================

class DebugRequest(BaseModel):

    code: str

    language: str

    stack_trace: str | None = None


# ==========================================================
# Documentation
# ==========================================================

class DocumentationRequest(BaseModel):

    code: str

    language: str


# ==========================================================
# Dependency Analyzer
# ==========================================================

class DependencyAnalyzerRequest(BaseModel):

    project_path: str


# ==========================================================
# Code Explainer
# ==========================================================

class CodeExplainerRequest(BaseModel):

    code: str

    language: str


# ==========================================================
# Test Generator
# ==========================================================

class TestGeneratorRequest(BaseModel):

    code: str

    language: str

    framework: str | None = None


# ==========================================================
# Git Assistant
# ==========================================================

class GitAssistantRequest(BaseModel):

    repository_path: str

    task: str = Field(
        description="Git task to perform."
    )


# ==========================================================
# Refactor
# ==========================================================

class RefactorRequest(BaseModel):

    code: str

    language: str

    objective: str


# ==========================================================
# Response
# ==========================================================

class CodingResponse(BaseModel):

    success: bool

    message: str