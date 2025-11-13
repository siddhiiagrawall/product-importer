# app/models.py
from sqlalchemy import (
    Table, Column, Integer, String, Text, Numeric, Boolean,
    DateTime, func, MetaData, UniqueConstraint
)
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255), nullable=False),
    Column("sku_lower", String(255), nullable=False),
    Column("name", String(512)),
    Column("description", Text),
    Column("price", Numeric(12, 2)),
    Column("active", Boolean, nullable=False, server_default="true"),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    UniqueConstraint("sku_lower", name="uq_products_sku_lower")
)


class Product:
    def __init__(self, sku, name=None, description=None, price=None, active=True):
        self.sku = sku
        self.sku_lower = sku.lower() if sku else None
        self.name = name
        self.description = description
        self.price = price
        self.active = active

    def to_dict(self):
        return {
            "id": getattr(self, "id", None),
            "sku": self.sku,
            "name": self.name,
            "description": self.description,
            "price": float(self.price) if self.price is not None else None,
            "active": self.active,
            "created_at": getattr(self, "created_at", None),
            "updated_at": getattr(self, "updated_at", None),
        }


mapper_registry.map_imperatively(Product, products)
