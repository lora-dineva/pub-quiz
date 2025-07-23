"""
CRUD (Create, Read, Update, Delete) operations for the database models.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.models import Question, QuestionType
from app.schemas import QuestionCreate, QuestionUpdate


def create_question(db: Session, question: QuestionCreate) -> Question:
    """Create a new question in the database."""
    db_question = Question(
        question_text=question.question_text,
        answer_text=question.answer_text,
        question_type=question.question_type,
        category=question.category,
        subcategory=question.subcategory,
        media_file_path=question.media_file_path
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(db: Session, question_id: uuid.UUID) -> Optional[Question]:
    """Get a question by ID."""
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    question_type: Optional[QuestionType] = None
) -> List[Question]:
    """Get questions with optional filtering."""
    query = db.query(Question)
    
    if category:
        query = query.filter(Question.category == category)
    
    if subcategory:
        query = query.filter(Question.subcategory == subcategory)
    
    if question_type:
        query = query.filter(Question.question_type == question_type)
    
    return query.offset(skip).limit(limit).all()


def update_question(
    db: Session,
    question_id: uuid.UUID,
    question_update: QuestionUpdate
) -> Optional[Question]:
    """Update a question."""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        return None
    
    update_data = question_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: uuid.UUID) -> bool:
    """Delete a question."""
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        return False
    
    db.delete(question)
    db.commit()
    return True


def get_questions_by_category(db: Session, category: str) -> List[Question]:
    """Get all questions for a specific category."""
    return db.query(Question).filter(Question.category == category).all()


def get_questions_by_subcategory(
    db: Session, 
    category: str, 
    subcategory: str
) -> List[Question]:
    """Get all questions for a specific subcategory."""
    return db.query(Question).filter(
        Question.category == category,
        Question.subcategory == subcategory
    ).all()


def get_questions_count(db: Session) -> int:
    """Get total count of questions."""
    return db.query(Question).count()


def get_questions_count_by_category(db: Session) -> dict:
    """Get count of questions grouped by category."""
    results = db.query(
        Question.category,
        db.func.count(Question.id).label('count')
    ).group_by(Question.category).all()
    
    return {result.category: result.count for result in results} 