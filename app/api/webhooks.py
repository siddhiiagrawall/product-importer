from fastapi import APIRouter

router = APIRouter()

@router.get("/webhooks")
async def list_webhooks():
    return {"webhooks": []}
