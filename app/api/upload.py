from fastapi import APIRouter, UploadFile, File
import uuid
import os
import json
import time
import redis
from sse_starlette.sse import EventSourceResponse

from app.tasks.importer import import_csv_task

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize Redis
r = redis.Redis.from_url(os.getenv("REDIS_URL"))

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{upload_id}.csv")

    # Save uploaded file to disk
    with open(path, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    # Trigger Celery async task
    import_csv_task.delay(upload_id, path)

    return {"upload_id": upload_id}


# ------------------------------
# ADD THIS: SSE Progress Endpoint
# ------------------------------

def progress_stream(upload_id: str):
    """ Generator that streams progress updates from Redis """
    while True:
        raw = r.get(f"progress:{upload_id}")
        if raw:
            data = raw.decode()
            yield f"data: {data}\n\n"

            parsed = json.loads(data)
            if parsed.get("status") == "complete":
                break

        time.sleep(1)


@router.get("/progress/{upload_id}/sse")
async def progress_sse(upload_id: str):
    return EventSourceResponse(progress_stream(upload_id))
