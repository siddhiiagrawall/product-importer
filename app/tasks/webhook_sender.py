from app.core.celery_app import celery
import httpx

@celery.task(name="send_webhook_task")
def send_webhook_task(url: str, payload: dict):
    try:
        httpx.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Webhook failed:", url, e)
