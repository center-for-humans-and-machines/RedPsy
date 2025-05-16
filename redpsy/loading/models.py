"""Data schemas for Pydantic validation."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Role(str, Enum):
    """Enum for conversation roles."""

    CLINICIAN = "clinician"
    COMPANION = "companion"


class ConversationType(str, Enum):
    """Enum for conversation types."""

    OPEN_ENDED = "open-ended"
    STANDARDIZED_SAFETY = "standardized-safety-evaluation"


# pylint: disable=too-few-public-methods
class RegTestPrompt(BaseModel):
    """Schema for regression test prompts."""

    Question: str = Field(..., min_length=1)
    Title: str = Field(..., min_length=1)
    Situation: str = Field(..., min_length=1)
    Ideal_Response: str = Field(..., min_length=1)


class ConversationMessage(BaseModel):
    """Schema for a single conversation message."""

    role: Role = Field(...)
    content: str = Field(..., min_length=1)
    turn: int = Field(..., ge=0)


class ConversationDataset(BaseModel):
    """Schema for conversation dataset entries."""

    conversation_id: str = Field(..., min_length=1)
    conversation: List[ConversationMessage] = Field(..., min_items=1)
    conversation_type: ConversationType = Field(...)
    model: str = Field(..., min_length=1)
    model_provider: str = Field(..., min_length=1)
    api_version: Optional[str] = None
    temperature: float = Field(..., ge=0.0, le=2.0)
    companion_system_prompt: str = Field(..., min_length=1)
    clinician_system_prompt: str = Field(..., min_length=1)
    created_at: datetime
    updated_at: datetime
    conversation_duration_s: float = Field(..., ge=0.0)
