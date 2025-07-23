"""
Database models for the Pub Quiz application using SQLAlchemy ORM.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import create_engine, Column, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class QuestionType(PyEnum):
    """Enumeration for different types of quiz questions."""
    OPEN = "open"
    TRUE_FALSE = "true_false"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Question(Base):
    """
    Question model representing a quiz question in the database.
    
    Attributes:
        id: Unique UUID identifier for the question
        question_text: The actual question text
        answer_text: The correct answer to the question
        question_type: Type of question (open, true_false, image, video, audio)
        category: Main category (e.g., History, Music, Movies)
        subcategory: Subcategory within the main category
        date_created: Timestamp when the question was created
        media_file_path: Optional path to media file for image/video/audio questions
    """
    
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    media_file_path = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<Question(id={self.id}, type={self.question_type.value}, category={self.category})>"
    
    def __str__(self):
        return f"{self.category} - {self.subcategory}: {self.question_text[:50]}..."


# Database engine and session configuration will be imported from database.py 