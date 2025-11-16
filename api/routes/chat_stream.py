# routers/chat_stream.py 或 api/routes/chat_stream.py（依你實際路徑）
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
import httpx
import os
import json

router = APIRouter()

GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_KEY = os.getenv("GROK_KEY")  # 記得在 Railway 設定環境變數

async def stream_grok(messages):
    if not GROK_KEY:
        # 沒設 key 直接丟錯訊息
        yield 'data: {"error":"GROK_API_KEY not set"}\n\n'
        yield "data: [DONE]\n\n"
        return

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
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
        ) as response:

            async for line in response.aiter_lines():
                if not line:
                    continue

                # Grok 回傳格式通常會是 "data: {...}"
                if line.startswith("data:"):
                    payload = line[len("data:"):].strip()

                    if payload == "[DONE]":
                        # 結束
                        yield "data: [DONE]\n\n"
                        break

                    # 原樣轉發 JSON 給前端
                    yield f"data: {payload}\n\n"


@router.post("/grok-stream")
async def grok_stream(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    return StreamingResponse(
        stream_grok(messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )