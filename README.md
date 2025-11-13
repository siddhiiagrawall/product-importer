# Product Importer Backend (FastAPI + Celery)

## Phase 1: Base Setup

This backend supports:
- FastAPI HTTP API
- Celery async worker
- Redis for task queue
- PostgreSQL for database

### Run Locally
1. Install Redis locally  
2. Install PostgreSQL locally  
3. Create `.env` file:
    DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/products_db
    REDIS_URL=redis://localhost:6379/0

4. Install dependencies:
pip install -r requirements.txt


5. Run FastAPI:
uvicorn app.main:app --reload


6. Start Celery worker:
celery -A app.core.celery_app.celery worker --loglevel=info

Visit:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health



