# scripts/create_tables.py
import sys
from pathlib import Path

# When running this file directly (python scripts/create_tables.py), Python
# adds the script's directory to sys.path, not the project root. That means
# top-level packages like `app` won't be found. Insert the project root
# (parent of the scripts/ folder) at the front of sys.path so `import app`
# works whether the file is run directly or as a module.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models import metadata
from app.db import engine

def create_all():
    print("Creating tables...")
    metadata.create_all(engine)
    print("Done.")

if __name__ == "__main__":
    create_all()
