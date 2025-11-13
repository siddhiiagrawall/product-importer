Product Importer — FastAPI + Celery + Redis + PostgreSQL

A scalable backend application for importing large CSV product files (up to 500,000 rows) with real-time progress tracking, a basic UI, and full async processing using Celery.

This app satisfies assignment requirements (Stories 1 & 1A):

File upload via UI

Asynchronous CSV processing

Upsert with SKU uniqueness

Real-time progress via SSE

Progress bar UI

PostgreSQL storage

Redis-backed event streaming

TECH STACK

Backend API: FastAPI
Async Worker: Celery
Message Broker: Redis
Database: PostgreSQL
ORM: SQLAlchemy
Realtime Updates: Server-Sent Events (SSE)
Frontend: Basic HTML + JS

PROJECT STRUCTURE

product-importer/

app/

main.py

api/

upload.py

progress.py

tasks/

importer.py

db.py

core/

celery_app.py

models.py

templates/

upload.html

static/

upload.js

styles.css

scripts/

create_tables.py

uploads/

.env

README.md

requirements.txt

SETUP INSTRUCTIONS

Create virtual environment (Windows)
py -3.11 -m venv venv
venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Create PostgreSQL database
Open psql and run:
CREATE DATABASE products_db;

Create tables
python scripts/create_tables.py

Start Redis (Windows)
Start redis-server in a separate terminal.

Start FastAPI server
uvicorn app.main:app --reload --port 8000

Start Celery worker
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo

FILE UPLOAD FLOW (Story 1)

User selects CSV file

File saved to /uploads

Celery async task processes the CSV

CSV processed in chunks of 10,000 rows

Rows inserted or upserted into PostgreSQL

Redis stores progress updates

UI shows real-time progress

REAL-TIME PROGRESS (Story 1A)

Frontend connects to:
GET /api/progress/{upload_id}/sse

Backend streams progress JSON:
{"percent": 34, "status": "processing"}

UI updates progress bar live.

UI

Open in browser:
http://127.0.0.1:8000/upload

Features:

File chooser

Upload button

Live progress bar

Status messages

TESTING

Create a test CSV file:

sku,name,description,price
SKU1,Product A,Description A,10.99
SKU2,Product B,Description B,20.50
SKU3,Product C,Description C,30.00

Upload via UI and watch the progress bar update.

FEATURES COMPLETED

Story 1 — File Upload: Completed
Story 1A — Upload Progress: Completed
Async CSV Processing: Completed
Chunked Insert with Upsert: Completed
SSE Streaming: Completed
Upload UI: Completed

NEXT PHASES

Story 2 — Product CRUD UI
Story 3 — Bulk Delete
Story 4 — Webhooks management
Deployment to Render
Final testing
Commit cleanup