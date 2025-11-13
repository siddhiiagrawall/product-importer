# scripts/create_tables.py
from app.models import metadata
from app.db import engine

def create_all():
    print("Creating tables...")
    metadata.create_all(engine)
    print("Done.")

if __name__ == "__main__":
    create_all()
