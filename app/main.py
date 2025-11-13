from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import upload, products, webhooks

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# --------------------
# UI ROUTES (Pages)
# --------------------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.get("/products")
def product_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

# --------------------
# API ROUTES (Backend)
# --------------------

app.include_router(upload.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
