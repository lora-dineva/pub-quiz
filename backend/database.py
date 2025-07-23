"""
Database configuration and connection management for the Pub Quiz application.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://quiz_user:quiz_password@localhost:5432/pub_quiz_db"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function to get database session.
    Use this in your application to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    create_tables()
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database() 