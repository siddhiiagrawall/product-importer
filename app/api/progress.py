import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import redis, os, json, time

router = APIRouter()

r = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True,
    ssl_cert_reqs=None
)

@router.get("/progress/{upload_id}/sse")
async def sse_progress(upload_id: str):

    async def event_stream():
        key = f"progress:{upload_id}"
        last_sent = None

        while True:
            val = r.get(key)
            if val and val != last_sent:
                yield f"{val}\n\n"
                last_sent = val

                # If upload is complete, stop streaming
                try:
                    obj = json.loads(val)
                    if obj.get("status") == "complete" or obj.get("percent") == 100:
                        yield "{\"percent\":100, \"status\":\"complete\"}\n\n"
                        break
                except:
                    pass

            # Keep-alive ping every second
            yield "ping\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
