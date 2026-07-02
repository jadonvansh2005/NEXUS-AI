"""
UPSS GitHub Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class GitHubProvider(str, Enum):

    GITHUB = "github"

    GITHUB_ENTERPRISE = "github_enterprise"


# ==========================================================
# Repository Search
# ==========================================================

class RepositorySearchRequest(BaseModel):

    query: str

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Clone Repository
# ==========================================================

class CloneRepositoryRequest(BaseModel):

    repository: str

    destination: str

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Commit
# ==========================================================

class CommitRequest(BaseModel):

    repository_path: str

    message: str

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Push
# ==========================================================

class PushRequest(BaseModel):

    repository_path: str

    remote: str = "origin"

    branch: str = "main"

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Pull Request
# ==========================================================

class PullRequestRequest(BaseModel):

    repository: str

    title: str

    body: str

    head: str

    base: str = "main"

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Issue
# ==========================================================

class IssueRequest(BaseModel):

    repository: str

    title: str

    body: str

    labels: list[str] = Field(
        default_factory=list,
    )

    provider: GitHubProvider = (
        GitHubProvider.GITHUB
    )


# ==========================================================
# Response
# ==========================================================

class GitHubResponse(BaseModel):

    success: bool

    message: str

    provider: str