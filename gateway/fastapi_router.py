from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import json

app = FastAPI()

VLLM_URL = "http://vllm:8000/v1/chat/completions"
EMBED_URL = "http://embeddings:80/embed"

@app.get("/")
def root():
    return {"status": "ai-dev-cloud running"}

@app.post("/embeddings")
async def embeddings(payload: dict):
    timeout = httpx.Timeout(120.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(EMBED_URL, json=payload)
        return r.json()

@app.post("/chat/stream")
async def chat_stream(payload: dict):
    """
    Streams tokens from vLLM back to the client in real-time.
    Expects OpenAI-style messages format:
    {
        "model": "deepseek-coder",
        "messages": [{"role": "user", "content": "Prompt text"}],
        "max_tokens": 512
    }
    """
    timeout = httpx.Timeout(None)  # disable client timeout for streaming

    async def event_generator():
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", VLLM_URL, json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            # vLLM streams JSON lines like {"choices":[{"delta":{"content":"text"}}]}
                            event = json.loads(line)
                            # Extract token content
                            token = event["choices"][0]["delta"].get("content")
                            if token:
                                yield token
                        except Exception:
                            # ignore non-JSON lines
                            continue

    return StreamingResponse(event_generator(), media_type="text/plain")
