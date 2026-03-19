# MDCP Data Backend (FastAPI)

This is the backend service for mdcp_data based on the defined architecture.

## Tech Stack
- Python 3.13.7
- FastAPI
- SQLAlchemy 2.0 (Async) + MySQL (aiomysql)
- MinIO
- Elasticsearch 8

## Setup Instructions

1. **Install Dependencies**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   Copy `.env.example` to `.env` and adjust the configuration as needed for your local databases and services.

3. **Run the Application**
   ```bash
   python scripts/run.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn services.dataset.main:app --reload
   ```

## API Documentation
Once running, visit `http://localhost:8000/docs` to see the generated Swagger UI.
The `/health` endpoint checks connections to MySQL, MinIO, and Elasticsearch.
