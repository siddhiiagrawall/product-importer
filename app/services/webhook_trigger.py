# app/services/webhook_trigger.py

import httpx
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import SessionLocal
from app.models import Webhook, webhooks


async def _send_webhook(url: str, payload: dict):
    """Send a webhook POST request asynchronously."""
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            await client.post(url, json=payload)
        except Exception:
            pass  # ignore individual failures


def trigger_event(event_name: str, payload: dict):
    """
    Trigger all active webhooks listening to a given event.
    This function:
    - fetches active webhooks from DB
    - dispatches async HTTP calls
    """

    db: Session = SessionLocal()
    try:
        stmt = select(Webhook).where(
            webhooks.c.event == event_name,
            webhooks.c.active == True
        )
        hooks = db.execute(stmt).scalars().all()

        for hook in hooks:
            # Fire and forget
            import asyncio
            asyncio.create_task(_send_webhook(hook.url, payload))

    finally:
        db.close()
