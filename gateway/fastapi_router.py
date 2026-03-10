from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json

app = FastAPI()

VLLM_URL = "http://vllm:8000/v1/chat/completions"
EMBED_URL = "http://embeddings:80/embed"

@app.get("/")
def root():
    return {"status": "swarm is ready to attack"}

@app.post("/embeddings")
async def embeddings(payload: dict):
    timeout = httpx.Timeout(120.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(EMBED_URL, json=payload)
        return r.json()

@app.post("/v1/chat/completions")
async def chat_stream(payload: dict):
    print("DEBUG PAYLOAD:", payload)
    payload["stream"] = True

    async def stream():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", VLLM_URL, json=payload) as r:
                async for chunk in r.aiter_bytes():
                    yield chunk

    return StreamingResponse(stream(), media_type="text/event-stream")
