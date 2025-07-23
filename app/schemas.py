"""
Pydantic schemas for request and response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

from backend.models import QuestionType


class QuestionBase(BaseModel):
    """Base schema for question data."""
    question_text: str = Field(..., min_length=1, max_length=2000, description="The question text")
    answer_text: str = Field(..., min_length=1, max_length=1000, description="The correct answer")
    question_type: QuestionType = Field(..., description="Type of question")
    category: str = Field(..., min_length=1, max_length=100, description="Question category")
    subcategory: str = Field(..., min_length=1, max_length=100, description="Question subcategory")
    media_file_path: Optional[str] = Field(None, max_length=500, description="Path to media file")


class QuestionCreate(QuestionBase):
    """Schema for creating a new question."""
    pass


class QuestionUpdate(BaseModel):
    """Schema for updating a question (all fields optional)."""
    question_text: Optional[str] = Field(None, min_length=1, max_length=2000)
    answer_text: Optional[str] = Field(None, min_length=1, max_length=1000)
    question_type: Optional[QuestionType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    subcategory: Optional[str] = Field(None, min_length=1, max_length=100)
    media_file_path: Optional[str] = Field(None, max_length=500)


class QuestionResponse(QuestionBase):
    """Schema for question responses."""
    id: uuid.UUID
    date_created: datetime
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """Schema for category responses."""
    categories: dict[str, list[str]] 