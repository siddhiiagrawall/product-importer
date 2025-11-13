from app.core.celery_app import celery

@celery.task(name="import_csv_task")
def import_csv_task(upload_id: str, file_path: str):
    print(f"[CELERY] Task started: {upload_id} | file: {file_path}")
    print("[CELERY] Processing dummy work...")
    print("[CELERY] Done.")
    return {"status": "completed", "upload_id": upload_id}
