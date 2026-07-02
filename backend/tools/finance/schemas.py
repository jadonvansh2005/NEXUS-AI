"""
UPSS Finance Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class FinanceProvider(str, Enum):

    GENERIC = "generic"

    YAHOO_FINANCE = "yahoo_finance"

    ALPHA_VANTAGE = "alpha_vantage"

    POLYGON = "polygon"

    FMP = "financial_modeling_prep"


# ==========================================================
# Expense Tracker
# ==========================================================

class ExpenseTrackerRequest(BaseModel):

    amount: float = Field(gt=0)

    category: str

    description: str | None = None

    date: str


# ==========================================================
# Budget Planner
# ==========================================================

class BudgetPlannerRequest(BaseModel):

    monthly_income: float = Field(gt=0)

    monthly_expenses: float = Field(ge=0)

    savings_goal: float = Field(ge=0)


# ==========================================================
# Investment Analyzer
# ==========================================================

class InvestmentAnalyzerRequest(BaseModel):

    symbol: str

    investment_amount: float = Field(gt=0)


# ==========================================================
# Portfolio Tracker
# ==========================================================

class PortfolioTrackerRequest(BaseModel):

    holdings: list[dict]


# ==========================================================
# Tax Estimator
# ==========================================================

class TaxEstimatorRequest(BaseModel):

    annual_income: float = Field(gt=0)

    country: str


# ==========================================================
# EMI Calculator
# ==========================================================

class EMICalculatorRequest(BaseModel):

    principal: float = Field(gt=0)

    annual_interest_rate: float = Field(ge=0)

    tenure_months: int = Field(gt=0)


# ==========================================================
# Invoice Generator
# ==========================================================

class InvoiceGeneratorRequest(BaseModel):

    client_name: str

    items: list[dict]

    currency: str = "INR"


# ==========================================================
# Financial Report
# ==========================================================

class FinancialReportRequest(BaseModel):

    title: str

    period: str


# ==========================================================
# Financial Planner
# ==========================================================

class FinancialPlannerRequest(BaseModel):

    monthly_income: float = Field(gt=0)

    financial_goal: str

    investment_horizon_years: int = Field(
        default=5,
        ge=1,
    )


# ==========================================================
# Response
# ==========================================================

class FinanceResponse(BaseModel):

    success: bool

    message: str