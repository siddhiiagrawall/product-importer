from fastapi import FastAPI
from app.api import upload, products, webhooks

app = FastAPI(title="Product Importer")

@app.get("/health")
async def health():
    return {"status": "ok"}

# Register routes
app.include_router(upload.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
