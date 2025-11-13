from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def list_products():
    return {"products": []}  # Filled in Phase 3
