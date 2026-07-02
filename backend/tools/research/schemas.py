"""
UPSS Research Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class ResearchProvider(str, Enum):

    GENERIC = "generic"

    GOOGLE_SCHOLAR = "google_scholar"

    ARXIV = "arxiv"

    SEMANTIC_SCHOLAR = "semantic_scholar"

    PUBMED = "pubmed"

    CROSSREF = "crossref"


# ==========================================================
# Web Research
# ==========================================================

class WebResearchRequest(BaseModel):

    query: str

    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
    )


# ==========================================================
# Paper Search
# ==========================================================

class PaperSearchRequest(BaseModel):

    query: str

    max_results: int = Field(
        default=10,
        ge=1,
        le=50,
    )

    provider: ResearchProvider = (
        ResearchProvider.GENERIC
    )


# ==========================================================
# Paper Summarizer
# ==========================================================

class PaperSummarizerRequest(BaseModel):

    paper_path: str


# ==========================================================
# Citation Generator
# ==========================================================

class CitationGeneratorRequest(BaseModel):

    title: str

    authors: list[str]

    year: int

    source: str

    style: str = "APA"


# ==========================================================
# Literature Review
# ==========================================================

class LiteratureReviewRequest(BaseModel):

    topic: str

    paper_limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )


# ==========================================================
# Fact Checker
# ==========================================================

class FactCheckerRequest(BaseModel):

    claim: str


# ==========================================================
# Note Generator
# ==========================================================

class NoteGeneratorRequest(BaseModel):

    text: str

    format: str = "bullet"


# ==========================================================
# Report Writer
# ==========================================================

class ReportWriterRequest(BaseModel):

    title: str

    content: str

    output_format: str = "pdf"


# ==========================================================
# Bibliography
# ==========================================================

class BibliographyRequest(BaseModel):

    citations: list[dict]

    style: str = "APA"


# ==========================================================
# Research Planner
# ==========================================================

class ResearchPlannerRequest(BaseModel):

    topic: str

    objective: str

    duration_weeks: int = Field(
        default=8,
        ge=1,
    )


# ==========================================================
# Response
# ==========================================================

class ResearchResponse(BaseModel):

    success: bool

    message: str