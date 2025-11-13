# app/api/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db_session, SessionLocal
from app.models import Product, products

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products")
def list_products(
    sku: Optional[str] = None,
    name: Optional[str] = None,
    active: Optional[bool] = None,
    page: int = 1,
    limit: int = 25,
    db: Session = Depends(get_db)
):
    stmt = select(Product)
    if sku:
        stmt = stmt.where(products.c.sku_lower == sku.lower())
    if name:
        stmt = stmt.where(products.c.name.ilike(f"%{name}%"))
    if active is not None:
        stmt = stmt.where(products.c.active == active)

    total = db.execute(select([products.c.id])).rowcount if False else None  # skip expensive total for now
    offset = (page - 1) * limit
    stmt = stmt.offset(offset).limit(limit)
    rows = db.execute(stmt).scalars().all()
    items = [r.to_dict() for r in rows]
    return {"items": items, "page": page, "limit": limit}

@router.post("/products")
def create_product(payload: dict, db: Session = Depends(get_db)):
    sku = payload.get("sku")
    if not sku:
        raise HTTPException(status_code=400, detail="sku required")
    prod = Product(sku=sku, name=payload.get("name"), description=payload.get("description"), price=payload.get("price"), active=payload.get("active", True))
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod.to_dict()

@router.put("/products/{product_id}")
def update_product(product_id: int, payload: dict, db: Session = Depends(get_db)):
    stmt = select(Product).where(products.c.id == product_id)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(404, "not found")
    for k in ("sku", "name", "description", "price", "active"):
        if k in payload:
            setattr(result, k, payload[k])
            if k == "sku":
                result.sku_lower = payload[k].lower()
    db.commit()
    db.refresh(result)
    return result.to_dict()

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    stmt = select(Product).where(products.c.id == product_id)
    result = db.execute(stmt).scalars().first()
    if not result:
        raise HTTPException(404, "not found")
    db.delete(result)
    db.commit()
    return {"status":"deleted"}
