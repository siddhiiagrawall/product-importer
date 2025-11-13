from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.api import upload, products, webhooks

app = FastAPI()

# Serve static files (JS/CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve templates
templates = Jinja2Templates(directory="app/templates")

# ROUTE FOR UPLOAD PAGE
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

app.include_router(upload.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(webhooks.router, prefix="/api")
