from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, Response
import httpx
import json
import sys
import os

# Ensure the root directory is in PYTHONPATH to import agents and tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import executor
from tools.definitions import TOOL_DEFINITIONS

app = FastAPI()

VLLM_URL = "http://vllm:8000"

@app.get("/")
def root():
    return {"status": "I'm ready to help papa"}

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.body()
    data = json.loads(body)
    
    # Use the executor to handle the request
    # For now, let's keep it simple and handle non-streaming via executor loop
    # If streaming is requested, we might need to handle it differently 
    # but the user asked to use the executor.
    
    messages = data.get("messages", [])
    model_name = data.get("model", "qwen3-coder")
    is_stream = data.get("stream", False)

    # Inject tool definitions if they are not provided by the client
    # or ensure they are consistent.
    tools = TOOL_DEFINITIONS if "tools" not in data else data["tools"]

    if not is_stream:
        result = await executor.run_executor_loop(messages, VLLM_URL, model_name, tools)
        
        # Strip <think> tags from final content if present
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0].get("message", {}).get("content", "")
            if content and "<think>" in content:
                import re
                content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
                result["choices"][0]["message"]["content"] = content
        
        return Response(content=json.dumps(result), media_type="application/json")
    else:
        async def stream_executor():
            current_messages = list(messages)
            async with httpx.AsyncClient(timeout=None) as client:
                payload = {
                    "model": model_name,
                    "messages": current_messages,
                    "tools": tools,
                    "tool_choice": "auto" if tools else None,
                    "stream": True
                }
                
                in_think = False
                async with client.stream("POST", f"{VLLM_URL}/v1/chat/completions", json=payload) as r:
                    async for chunk in r.aiter_bytes():
                        # Restore <think> stripping logic
                        if b"<think>" in chunk:
                            in_think = True
                            if b"</think>" in chunk:
                                parts = chunk.split(b"<think>", 1)
                                prefix = parts[0]
                                remainder = parts[1].split(b"</think>", 1)
                                suffix = remainder[1] if len(remainder) > 1 else b""
                                chunk = prefix + suffix
                                in_think = False
                            else:
                                chunk = chunk.split(b"<think>", 1)[0]
                        elif b"</think>" in chunk:
                            in_think = False
                            chunk = chunk.split(b"</think>", 1)[1]
                        elif in_think:
                            continue
                        
                        if chunk and not in_think:
                            yield chunk

        return StreamingResponse(stream_executor(), media_type="text/event-stream")

@app.api_route("/v1/{path:path}", methods=["GET", "POST"])
async def proxy(path: str, request: Request):
    # Proxy all other /v1/ requests directly to vLLM (e.g., /v1/models)
    url = f"{VLLM_URL}/v1/{path}"
    body = await request.body()
    method = request.method
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ["host", "content-length"]
    }

    async with httpx.AsyncClient(timeout=None) as client:
        r = await client.request(method, url, content=body, headers=headers)
        return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type"))
