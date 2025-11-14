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
# Add SSL required by Upstash
celery.conf.broker_transport_options = {
    "ssl": {
        "ssl_cert_reqs": "CERT_NONE"
    }
}

celery.conf.redis_backend_use_ssl = {
    "ssl_cert_reqs": "CERT_NONE"
}
celery.conf.update(
    task_routes={
        "app.tasks.*": {"queue": "default"}
    },
    task_track_started=True,
)
