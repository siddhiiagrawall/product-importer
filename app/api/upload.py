from fastapi import APIRouter, UploadFile, File
import uuid
import os
from app.tasks.importer import import_csv_task

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
