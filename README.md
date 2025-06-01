# FastAPI Project

A modern FastAPI application with best practices and configurations.

## Requirements

- Python 3.13+
- Poetry

## Project Structure

```
app/
├── api/            # API endpoints
│   └── endpoints/  # API route handlers
├── core/           # Application configuration
├── db/             # Database models and connection
├── models/         # Pydantic models
├── schemas/        # Pydantic schemas
└── services/       # Business logic
```

## Setup

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Running the Application

Start the development server:
```bash
poetry run uvicorn app.main:app --reload
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc

## Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint

## Features

- FastAPI with modern Python features
- CORS middleware configured
- Automatic API documentation
- Health check endpoint
- Poetry for dependency management
- Well-structured project layout 