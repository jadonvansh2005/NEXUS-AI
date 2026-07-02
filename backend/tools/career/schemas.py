"""
UPSS Career Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class CareerProvider(str, Enum):

    GENERIC = "generic"

    LINKEDIN = "linkedin"

    INDEED = "indeed"

    NAUKRI = "naukri"

    INTERNSHALA = "internshala"

    GITHUB = "github"


# ==========================================================
# Resume Analyzer
# ==========================================================

class ResumeAnalyzerRequest(BaseModel):

    resume_path: str


# ==========================================================
# ATS Score
# ==========================================================

class ATSScoreRequest(BaseModel):

    resume_path: str

    job_description: str | None = None


# ==========================================================
# Resume Builder
# ==========================================================

class ResumeBuilderRequest(BaseModel):

    personal_information: dict

    education: list[dict]

    experience: list[dict] = Field(
        default_factory=list,
    )

    skills: list[str] = Field(
        default_factory=list,
    )

    projects: list[dict] = Field(
        default_factory=list,
    )


# ==========================================================
# Job Search
# ==========================================================

class JobSearchRequest(BaseModel):

    keywords: str

    location: str

    experience_level: str = "fresher"

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    provider: CareerProvider = (
        CareerProvider.GENERIC
    )


# ==========================================================
# Internship Search
# ==========================================================

class InternshipSearchRequest(BaseModel):

    keywords: str

    location: str

    stipend_required: bool = False

    limit: int = Field(
        default=10,
        ge=1,
        le=100,
    )

    provider: CareerProvider = (
        CareerProvider.INTERNSHALA
    )


# ==========================================================
# LinkedIn Optimizer
# ==========================================================

class LinkedInOptimizerRequest(BaseModel):

    profile: dict


# ==========================================================
# Cover Letter
# ==========================================================

class CoverLetterRequest(BaseModel):

    company: str

    position: str

    resume_summary: str


# ==========================================================
# Interview Questions
# ==========================================================

class InterviewQuestionsRequest(BaseModel):

    role: str

    experience_level: str = "fresher"

    number_of_questions: int = Field(
        default=20,
        ge=1,
        le=100,
    )


# ==========================================================
# Skill Gap
# ==========================================================

class SkillGapRequest(BaseModel):

    current_skills: list[str]

    target_role: str


# ==========================================================
# Learning Path
# ==========================================================

class LearningPathRequest(BaseModel):

    target_role: str

    current_skills: list[str]


# ==========================================================
# Portfolio Review
# ==========================================================

class PortfolioReviewRequest(BaseModel):

    portfolio_url: str


# ==========================================================
# Response
# ==========================================================

class CareerResponse(BaseModel):

    success: bool

    message: str