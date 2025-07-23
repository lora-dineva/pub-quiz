"""
Main FastAPI application for the Pub Quiz backend.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from backend.database import get_db, init_database
from backend.models import Question, QuestionType
from backend.categories import QUIZ_CATEGORIES, is_valid_category, is_valid_subcategory
from app.schemas import QuestionCreate, QuestionResponse, QuestionUpdate

# Initialize FastAPI app
app = FastAPI(
    title="Pub Quiz API",
    description="Backend API for managing pub quiz questions",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Pub Quiz API",
        "version": "1.0.0",
        "docs": "/docs",
        "categories": list(QUIZ_CATEGORIES.keys())
    }


@app.get("/categories")
async def get_categories():
    """Get all available categories and subcategories."""
    return QUIZ_CATEGORIES


@app.post("/questions/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    """Create a new quiz question."""
    
    # Validate category and subcategory
    if not is_valid_category(question.category):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category: {question.category}"
        )
    
    if not is_valid_subcategory(question.category, question.subcategory):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid subcategory: {question.subcategory} for category: {question.category}"
        )
    
    # Create new question
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


@app.get("/questions/", response_model=List[QuestionResponse])
async def get_questions(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    question_type: Optional[QuestionType] = None,
    db: Session = Depends(get_db)
):
    """Get questions with optional filtering."""
    
    query = db.query(Question)
    
    if category:
        query = query.filter(Question.category == category)
    
    if subcategory:
        query = query.filter(Question.subcategory == subcategory)
    
    if question_type:
        query = query.filter(Question.question_type == question_type)
    
    questions = query.offset(skip).limit(limit).all()
    return questions


@app.get("/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str, db: Session = Depends(get_db)):
    """Get a specific question by ID."""
    
    try:
        question_uuid = uuid.UUID(question_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    question = db.query(Question).filter(Question.id == question_uuid).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question


@app.put("/questions/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: str,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """Update a specific question."""
    
    try:
        question_uuid = uuid.UUID(question_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    question = db.query(Question).filter(Question.id == question_uuid).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Update fields if provided
    update_data = question_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    
    return question


@app.delete("/questions/{question_id}")
async def delete_question(question_id: str, db: Session = Depends(get_db)):
    """Delete a specific question."""
    
    try:
        question_uuid = uuid.UUID(question_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    
    question = db.query(Question).filter(Question.id == question_uuid).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    db.delete(question)
    db.commit()
    
    return {"message": "Question deleted successfully"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 