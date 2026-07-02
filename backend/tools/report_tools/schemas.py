"""
UPSS Report Tool Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Report Format
# ==========================================================

class ReportFormat(str, Enum):

    PDF = "pdf"

    EXCEL = "xlsx"

    POWERPOINT = "pptx"

    HTML = "html"


# ==========================================================
# PDF Report
# ==========================================================

class PDFReportRequest(BaseModel):

    title: str

    content: str

    output_path: str = "report.pdf"


# ==========================================================
# Excel Report
# ==========================================================

class ExcelReportRequest(BaseModel):

    title: str

    data: list[dict]

    output_path: str = "report.xlsx"


# ==========================================================
# PowerPoint Report
# ==========================================================

class PPTReportRequest(BaseModel):

    title: str

    slides: list[dict]

    output_path: str = "report.pptx"


# ==========================================================
# Charts
# ==========================================================

class ChartRequest(BaseModel):

    title: str

    chart_type: str = Field(
        default="bar",
    )

    data: list[dict]

    output_path: str = "chart.png"


# ==========================================================
# Response
# ==========================================================

class ReportResponse(BaseModel):

    success: bool

    message: str

    output_path: str