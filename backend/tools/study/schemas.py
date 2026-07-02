"""
UPSS Study Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class StudyProvider(str, Enum):

    GENERIC = "generic"

    KHAN_ACADEMY = "khan_academy"

    COURSERA = "coursera"

    EDX = "edx"

    NPTEL = "nptel"

    YOUTUBE = "youtube"


# ==========================================================
# Concept Explainer
# ==========================================================

class ConceptExplainerRequest(BaseModel):

    topic: str

    level: str = "beginner"


# ==========================================================
# Study Planner
# ==========================================================

class StudyPlannerRequest(BaseModel):

    goal: str

    available_hours_per_day: float

    duration_days: int = Field(
        default=30,
        ge=1,
    )


# ==========================================================
# Quiz Generator
# ==========================================================

class QuizGeneratorRequest(BaseModel):

    topic: str

    difficulty: str = "medium"

    number_of_questions: int = Field(
        default=10,
        ge=1,
        le=100,
    )


# ==========================================================
# Flashcard Generator
# ==========================================================

class FlashcardGeneratorRequest(BaseModel):

    text: str


# ==========================================================
# Assignment Helper
# ==========================================================

class AssignmentHelperRequest(BaseModel):

    assignment: str

    subject: str


# ==========================================================
# Homework Solver
# ==========================================================

class HomeworkSolverRequest(BaseModel):

    question: str

    subject: str


# ==========================================================
# Practice Questions
# ==========================================================

class PracticeQuestionRequest(BaseModel):

    topic: str

    difficulty: str = "medium"

    count: int = Field(
        default=10,
        ge=1,
        le=100,
    )


# ==========================================================
# Revision Planner
# ==========================================================

class RevisionPlannerRequest(BaseModel):

    subjects: list[str]

    exam_date: str


# ==========================================================
# Learning Roadmap
# ==========================================================

class LearningRoadmapRequest(BaseModel):

    target_skill: str

    current_level: str = "beginner"


# ==========================================================
# Exam Preparation
# ==========================================================

class ExamPreparationRequest(BaseModel):

    exam_name: str

    subjects: list[str]

    exam_date: str


# ==========================================================
# Response
# ==========================================================

class StudyResponse(BaseModel):

    success: bool

    message: str