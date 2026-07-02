"""
UPSS Communication Schemas
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


# ==========================================================
# Provider
# ==========================================================

class CommunicationProvider(str, Enum):

    GENERIC = "generic"

    WHATSAPP = "whatsapp"

    DISCORD = "discord"

    SLACK = "slack"

    TEAMS = "teams"

    SMS = "sms"


# ==========================================================
# Message Composer
# ==========================================================

class MessageComposerRequest(BaseModel):

    recipient: str

    purpose: str

    tone: str = "professional"

    additional_context: str | None = None


# ==========================================================
# Message Rewriter
# ==========================================================

class MessageRewriterRequest(BaseModel):

    message: str

    tone: str = "professional"


# ==========================================================
# Translator
# ==========================================================

class TranslatorRequest(BaseModel):

    text: str

    source_language: str

    target_language: str


# ==========================================================
# Grammar Checker
# ==========================================================

class GrammarCheckerRequest(BaseModel):

    text: str


# ==========================================================
# Tone Converter
# ==========================================================

class ToneConverterRequest(BaseModel):

    text: str

    target_tone: str


# ==========================================================
# Meeting Summary
# ==========================================================

class MeetingSummaryRequest(BaseModel):

    transcript: str

    include_action_items: bool = True


# ==========================================================
# WhatsApp
# ==========================================================

class WhatsAppRequest(BaseModel):

    recipient: str

    message: str


# ==========================================================
# Discord
# ==========================================================

class DiscordRequest(BaseModel):

    channel_id: str

    message: str


# ==========================================================
# Slack
# ==========================================================

class SlackRequest(BaseModel):

    channel: str

    message: str


# ==========================================================
# Teams
# ==========================================================

class TeamsRequest(BaseModel):

    channel: str

    message: str


# ==========================================================
# SMS
# ==========================================================

class SMSRequest(BaseModel):

    phone_number: str

    message: str


# ==========================================================
# Planner
# ==========================================================

class CommunicationPlannerRequest(BaseModel):

    objective: str

    recipients: list[str] = Field(default_factory=list)

    preferred_channels: list[str] = Field(default_factory=list)


# ==========================================================
# Response
# ==========================================================

class CommunicationResponse(BaseModel):

    success: bool

    message: str