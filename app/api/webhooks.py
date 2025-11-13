from fastapi import APIRouter, Depends, HTTPException
from typing import List
import httpx
import time

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import SessionLocal
from app.models import webhooks, Webhook

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------
# LIST WEBHOOKS
# ------------------------------
@router.get("/webhooks")
def list_webhooks(db: Session = Depends(get_db)):
    rows = db.execute(select(Webhook)).scalars().all()
    return [w.to_dict() for w in rows]


# ------------------------------
# CREATE WEBHOOK
# ------------------------------
@router.post("/webhooks")
def create_webhook(payload: dict, db: Session = Depends(get_db)):
    url = payload.get("url")
    event = payload.get("event")
    active = payload.get("active", True)

    if not url or not event:
        raise HTTPException(400, "url and event are required")

    w = Webhook(url=url, event=event, active=active)
    db.add(w)
    db.commit()
    db.refresh(w)
    return w.to_dict()


# ------------------------------
# UPDATE WEBHOOK
# ------------------------------
@router.put("/webhooks/{webhook_id}")
def update_webhook(webhook_id: int, payload: dict, db: Session = Depends(get_db)):
    stmt = select(Webhook).where(webhooks.c.id == webhook_id)
    item = db.execute(stmt).scalars().first()

    if not item:
        raise HTTPException(404, "Webhook not found")

    for key in ["url", "event", "active"]:
        if key in payload:
            setattr(item, key, payload[key])

    db.commit()
    db.refresh(item)
    return item.to_dict()


# ------------------------------
# DELETE WEBHOOK
# ------------------------------
@router.delete("/webhooks/{webhook_id}")
def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    stmt = select(Webhook).where(webhooks.c.id == webhook_id)
    item = db.execute(stmt).scalars().first()

    if not item:
        raise HTTPException(404, "Webhook not found")

    db.delete(item)
    db.commit()
    return {"status": "deleted"}


# ------------------------------
# TEST WEBHOOK
# ------------------------------
@router.post("/webhooks/{webhook_id}/test")
async def test_webhook(webhook_id: int, db: Session = Depends(get_db)):
    stmt = select(Webhook).where(webhooks.c.id == webhook_id)
    item = db.execute(stmt).scalars().first()

    if not item:
        raise HTTPException(404, "Webhook not found")

    start = time.time()

    async with httpx.AsyncClient(timeout=5) as client:
        try:
            resp = await client.post(item.url, json={"test": "ok"})

            duration = round((time.time() - start) * 1000, 2)

            return {
                "status": "success",
                "http_status": resp.status_code,
                "response_time_ms": duration,
            }
        except Exception as e:
            duration = round((time.time() - start) * 1000, 2)
            return {
                "status": "failed",
                "error": str(e),
                "response_time_ms": duration,
            }
