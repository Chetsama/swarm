from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json

app = FastAPI()

VLLM_URL = "http://vllm:8000"

@app.api_route("/v1/{path:path}", methods=["GET", "POST"])
async def proxy(path: str, request: Request):

    url = f"{VLLM_URL}/v1/{path}"
    body = await request.body()

    # Handle Zed/vLLM compatibility
    if request.method == "POST":
        try:
            data = json.loads(body)

            # Flatten structured content [ {"type": "text", "text": "..."} ]
            if "messages" in data:
                for msg in data["messages"]:
                    if isinstance(msg.get("content"), list):
                        msg["content"] = "\n".join([
                            c.get("text", "") for c in msg["content"]
                            if isinstance(c, dict) and c.get("type") == "text"
                        ])

            # Zed sends tools by default; strip them to avoid vLLM requirement errors
            data.pop("tool_choice", None)
            data.pop("tools", None)

            body = json.dumps(data).encode()
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    async def stream_response():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                request.method,
                url,
                content=body,
                headers={
                    k: v for k, v in request.headers.items()
                    if k.lower() not in ["host", "content-length"]
                },
            ) as r:
                async for chunk in r.aiter_raw():
                    yield chunk

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream"
    )
