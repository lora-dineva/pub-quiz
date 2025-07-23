# Pub Quiz Backend

A comprehensive backend system for managing pub quiz questions built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- ✅ **Database Schema**: PostgreSQL with SQLAlchemy ORM
- ✅ **Question Management**: Full CRUD operations for quiz questions
- ✅ **Question Types**: Support for open, true/false, image, video, and audio questions
- ✅ **Categories & Subcategories**: Organized question classification system
- ✅ **Media Storage**: Local file storage for images, videos, and audio files
- ✅ **UUID Support**: Unique identifiers for all questions
- ✅ **Docker Orchestration**: Complete Docker Compose setup
- ✅ **RESTful API**: FastAPI with automatic OpenAPI documentation
- ✅ **Data Validation**: Pydantic schemas for request/response validation

## Project Structure

```
pub-quiz/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   └── schemas.py        # Pydantic schemas
├── backend/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # Database configuration
│   ├── categories.py     # Categories dictionary
│   └── crud.py          # Database operations
├── media/
│   ├── images/          # Image files storage
│   ├── videos/          # Video files storage
│   └── audio/           # Audio files storage
├── docker-compose.yml   # Docker orchestration
├── Dockerfile          # Backend container
├── requirements.txt    # Python dependencies
├── init.sql           # Database initialization
├── environment.template # Environment variables template
└── README.md          # This file
```

## Question Categories

| Category    | Subcategories                          |
| ----------- | -------------------------------------- |
| History     | Ancient, Medieval, Modern, World Wars  |
| Music       | Pop, Rock, Classical, Jazz, 90s        |
| Movies      | Action, Comedy, Drama, Horror          |
| Sports      | Football, Basketball, Olympics, Tennis |
| Science     | Physics, Chemistry, Biology, Astronomy |
| Literature  | Novels, Poetry, Plays, Authors         |
| Geography   | Countries, Capitals, Flags, Mountains  |
| Pop Culture | Celebrities, Memes, TV Shows, Trends   |
| Technology  | Computers, AI, Internet, Gadgets       |

## Question Types

- **open**: Open-ended text questions
- **true_false**: True/False questions
- **image**: Questions with image media
- **video**: Questions with video media
- **audio**: Questions with audio media

## Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd pub-quiz
   ```

2. **Start the services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - pgAdmin (optional): http://localhost:5050

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL:**
   - Install PostgreSQL
   - Create database and user as specified in `init.sql`

3. **Configure environment:**
   ```bash
   cp environment.template .env
   # Edit .env with your database credentials
   ```

4. **Initialize database:**
   ```bash
   python -m backend.database
   ```

5. **Run the application:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Base Endpoints
- `GET /` - API information and available categories
- `GET /health` - Health check
- `GET /categories` - Get all categories and subcategories

### Question Management
- `POST /questions/` - Create a new question
- `GET /questions/` - Get questions (with optional filtering)
- `GET /questions/{question_id}` - Get a specific question
- `PUT /questions/{question_id}` - Update a question
- `DELETE /questions/{question_id}` - Delete a question

### Query Parameters for GET /questions/
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum number of records to return
- `category`: Filter by category
- `subcategory`: Filter by subcategory
- `question_type`: Filter by question type

## Example API Usage

### Create a Question
```bash
curl -X POST "http://localhost:8000/questions/" \
     -H "Content-Type: application/json" \
     -d '{
       "question_text": "What is the capital of France?",
       "answer_text": "Paris",
       "question_type": "open",
       "category": "Geography",
       "subcategory": "Capitals"
     }'
```

### Get Questions by Category
```bash
curl "http://localhost:8000/questions/?category=History&limit=10"
```

## Database Schema

### Question Table
| Field            | Type        | Description                        |
|------------------|-------------|------------------------------------|
| id               | UUID        | Primary key (auto-generated)      |
| question_text    | Text        | The question text                  |
| answer_text      | Text        | The correct answer                 |
| question_type    | Enum        | Type of question                   |
| category         | String(100) | Main category                      |
| subcategory      | String(100) | Subcategory                        |
| date_created     | DateTime    | Creation timestamp                 |
| media_file_path  | String(500) | Optional media file path           |

## Docker Services

- **postgres**: PostgreSQL 15 database server
- **backend**: FastAPI application server
- **pgadmin**: Web-based PostgreSQL administration (optional)

## Environment Variables

See `environment.template` for all available configuration options.

## Development

### Adding New Categories
1. Edit `backend/categories.py`
2. Add new categories to the `QUIZ_CATEGORIES` dictionary

### Adding New Question Types
1. Edit `backend/models.py`
2. Add new values to the `QuestionType` enum

### Database Migrations
When modifying models, you may need to recreate the database:
```bash
docker-compose down -v  # Remove volumes
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue in the GitHub repository.
