# app/tasks/importer.py

import os
import csv
import io
import json
import time
from typing import Tuple
from app.core.celery_app import celery
from app.db import engine
import redis
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
r = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True,
    ssl_cert_reqs=None
)

CHUNK_SIZE = 5000  # smaller chunk = smoother progress updates

def publish_progress(upload_id: str, percent: int, status: str):
    key = f"progress:{upload_id}"
    payload = {"percent": percent, "status": status}
    r.set(key, json.dumps(payload))

    # Optionally publish (UI may use Redis pub/sub later)
    try:
        r.publish(f"upload:{upload_id}", json.dumps(payload))
    except:
        pass


# ✨ CLEAN A ROW FOR COPY (removes BOM, NULL bytes, invalid chars)
def clean_row(row):
    cleaned = []
    for col in row:
        if col is None:
            cleaned.append("")
        else:
            c = col.replace("\x00", "")      # remove nulls
            c = c.replace("\ufeff", "")      # remove BOM
            cleaned.append(c)
    return cleaned


@celery.task(name="import_csv_task", bind=True)
def import_csv_task(self, upload_id: str, file_path: str):

    publish_progress(upload_id, 0, "starting")

    try:
        # Count number of lines
        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            total_lines = sum(1 for _ in fh) - 1  # subtract header

        if total_lines <= 0:
            publish_progress(upload_id, 100, "complete")
            return {"status": "no_data", "upload_id": upload_id}

        processed = 0
        publish_progress(upload_id, 1, "processing")

        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)  # skip header
            chunk = []

            for row in reader:
                cleaned = clean_row(row)
                chunk.append(cleaned)

                if len(chunk) >= CHUNK_SIZE:
                    _process_chunk(engine, chunk)
                    processed += len(chunk)

                    percent = int((processed / total_lines) * 100)
                    publish_progress(upload_id, percent, "processing")

                    chunk = []

            # last chunk
            if chunk:
                _process_chunk(engine, chunk)
                processed += len(chunk)

                percent = int((processed / total_lines) * 100)
                publish_progress(upload_id, percent, "processing")


        publish_progress(upload_id, 100, "complete")
        return {"status": "completed", "upload_id": upload_id}

    except Exception as exc:
        # Report the failure to UI
        publish_progress(upload_id, 0, f"error: {str(exc)}")
        raise


def _process_chunk(engine, rows):
    conn = engine.raw_connection()

    try:
        cur = conn.cursor()

        # staging table
        cur.execute("""
            CREATE TEMP TABLE tmp_products (
                sku text,
                name text,
                description text,
                price numeric
            ) ON COMMIT DROP;
        """)

        # write CSV into memory
        sio = io.StringIO()
        writer = csv.writer(sio)

        for r in rows:
            # Ensure exactly 4 fields
            while len(r) < 4:
                r.append("")
            writer.writerow(r[:4])

        sio.seek(0)

        # COPY IN
        cur.copy_expert("""
            COPY tmp_products (sku, name, description, price)
            FROM STDIN WITH (FORMAT csv)
        """, sio)

        # UPSERT
        cur.execute("""
            INSERT INTO products (
                sku, sku_lower, name, description, price, active, created_at, updated_at
            )
            SELECT 
                sku, lower(sku), name, description, price, 
                true, now(), now()
            FROM tmp_products
            ON CONFLICT (sku_lower)
            DO UPDATE SET
                sku = EXCLUDED.sku,
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                price = EXCLUDED.price,
                updated_at = now();
        """)

        conn.commit()

    finally:
        try: cur.close()
        except: pass
        try: conn.close()
        except: pass
