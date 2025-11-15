from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx
import json
import asyncio

router = APIRouter()

GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_KEY = "YOUR_GROK_API_KEY"

async def stream_grok(messages):
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.stream(
            "POST",
            GROK_API_URL,
            headers={
                "Authorization": f"Bearer {GROK_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "grok-beta",
                "messages": messages,
                "stream": True,
            },
        )

        async for line in response.aiter_lines():
            if line.strip().startswith("data:"):
                data = line.replace("data:", "").strip()
                if data == "[DONE]":
                    yield "data: [DONE]\n\n"
                    break

                try:
                    delta = json.loads(data)["choices"][0]["delta"]
                    if "content" in delta:
                        chunk = delta["content"]
                        yield f"data: {json.dumps(chunk)}\n\n"
                except:
                    continue


@router.post("/grok-stream")
async def grok_stream(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    return StreamingResponse(
        stream_grok(messages),
        media_type="text/event-stream",
    )