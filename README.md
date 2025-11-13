Product Importer — FastAPI + Celery + Redis + PostgreSQL

A scalable backend for importing large CSV product files (tested to 500,000 rows) with real-time progress tracking, a small UI, and asynchronous processing via Celery.

This repository implements the assignment stories 1, 1A, 2, 3 and 4 (all stories completed):

- File upload via a simple UI
- Asynchronous CSV processing with Celery
- Upsert behavior using SKU as the unique key
- Real-time progress updates via Server-Sent Events (SSE)

Tech stack

- Backend: FastAPI
- Worker: Celery
- Broker: Redis
- Database: PostgreSQL
- ORM: SQLAlchemy
- Realtime: Server-Sent Events (SSE)
- Frontend: Minimal HTML + JS

Project layout (top-level)

app/
	├─ api/           # API endpoints
	├─ tasks/         # Celery task implementations
	├─ core/          # Celery app / config
	├─ models.py      # SQLAlchemy models
	├─ db.py          # Database utilities
	└─ main.py        # FastAPI application entry

scripts/
	└─ create_tables.py

uploads/            # Stored uploaded CSVs (gitignored)

README.md
requirements.txt

Setup (Windows)

1. Create and activate a virtual environment

```powershell
py -3.11 -m venv venv
venv\Scripts\Activate.ps1  # PowerShell
# or: venv\Scripts\activate.bat  (cmd.exe)
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Create the PostgreSQL database (psql)

```sql
CREATE DATABASE products_db;
```

4. Create database tables

```powershell
python scripts/create_tables.py
```

5. Start Redis

On Windows you can run redis-server (WSL or a native build). Start it in a separate terminal.

6. Start the FastAPI server

```powershell
uvicorn app.main:app --reload --port 8000
```

7. Start a Celery worker (use the solo pool on Windows)

```powershell
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo
```

File upload flow (story 1)

1. User selects a CSV file in the upload UI
2. The file is saved to `uploads/`
3. A Celery task processes the CSV in the background (chunked inserts)
4. Rows are inserted or upserted into PostgreSQL using SKU uniqueness
5. Progress updates are published to Redis and streamed to clients via SSE

Realtime progress (story 1A)

The frontend connects to an SSE endpoint such as:

GET /api/progress/{upload_id}/sse

The server sends JSON progress events, for example:

{"percent": 34, "status": "processing"}

UI

Open the upload page in your browser:

http://127.0.0.1:8000/upload

Features

- File chooser and upload button
- Live progress bar updated via SSE
- Status messages

Testing

Create a small CSV to verify behavior:

sku,name,description,price
SKU1,Product A,Description A,10.99
SKU2,Product B,Description B,20.50
SKU3,Product C,Description C,30.00

Upload it through the UI and observe the progress bar.


Completed items

- Story 1 — File upload: Completed
- Story 1A — Upload progress: Completed
- Story 2 — Product CRUD UI: Completed
- Story 3 — Bulk delete: Completed
- Story 4 — Webhooks management: Completed
- Asynchronous CSV processing: Completed
- Chunked insert with upsert: Completed
- SSE streaming: Completed
- Upload UI: Completed

Next phases

- Optional improvements & maintenance: deployment automation, additional end-to-end tests, monitoring, and small UX refinements (no outstanding assignment stories remain).

Notes

- Rename `requirments.txt` to `requirements.txt` if present. I updated the README to reference `requirements.txt`.
- Ensure `uploads/` is in `.gitignore` so uploaded files are not committed.

If you want, I can also create a `.gitignore` and rename the file on disk.