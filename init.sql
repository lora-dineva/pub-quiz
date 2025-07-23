-- Database initialization script for Pub Quiz application
-- This file is executed when the PostgreSQL container starts for the first time

-- Create the database (if not exists)
CREATE DATABASE pub_quiz_db;

-- Connect to the database
\c pub_quiz_db;

-- Create the quiz_user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'quiz_user') THEN
        CREATE USER quiz_user WITH PASSWORD 'quiz_password';
    END IF;
END
$$;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE pub_quiz_db TO quiz_user;
GRANT ALL ON SCHEMA public TO quiz_user;

-- Create UUID extension (required for UUID fields)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Add any initial data or constraints here if needed
-- (Tables will be created automatically by SQLAlchemy) 