from app.core.celery_app import celery
import redis
import os

r = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True,
    ssl_cert_reqs=None
)


@celery.task(bind=True)
def import_csv_task(self, upload_id, filepath):
    channel = f"upload:{upload_id}"

    # Dummy progress (will implement real logic in Phase 2)
    r.publish(channel, "0|started")
    r.publish(channel, "50|processing")
    r.publish(channel, "100|complete")

    return True
