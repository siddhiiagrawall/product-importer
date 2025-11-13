from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER = os.getenv("REDIS_URL")
CELERY_BACKEND = os.getenv("REDIS_URL")

celery = Celery(
    "product_importer",
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND,
    include=["app.tasks.importer"],
)

celery.conf.update(
    task_routes={
        "app.tasks.*": {"queue": "default"}
    },
    task_track_started=True,
)
