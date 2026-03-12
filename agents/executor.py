from tools import filesystem, shell, git
import json

async def execute_tool_call(tool_call):
    """
    Executes a structured tool call (OpenAI-style).
    """
    name = tool_call.get("function", {}).get("name")
    args_raw = tool_call.get("function", {}).get("arguments", "{}")
    
    try:
        args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON in arguments: {args_raw}"}

    try:
        if name == "list_files":
            return {"result": filesystem.list_files(args.get("path", "."))}
        
        elif name == "read_file":
            return {"result": filesystem.read_file(args.get("path"))}
        
        elif name == "write_file":
            filesystem.write_file(args.get("path"), args.get("content"))
            return {"result": f"wrote to {args.get('path')}"}
        
        elif name == "run_command":
            return {"result": shell.run_command(args.get("cmd"))}
        
        elif name == "git_status":
            return {"result": git.git_status()}
        
        elif name == "git_diff":
            return {"result": git.git_diff()}
        
        else:
            return {"error": f"Tool not found: {name}"}

    except Exception as e:
        return {"error": str(e)}

async def run_executor_loop(messages, vllm_url, model_name, tools):
    """
    Simple loop that calls vLLM and executes tool calls until a final answer is produced.
    """
    import httpx
    
    async with httpx.AsyncClient(timeout=None) as client:
        current_messages = list(messages)
        
        while True:
            # Call vLLM
            payload = {
                "model": model_name,
                "messages": current_messages,
                "tools": tools,
                "tool_choice": "auto" if tools else None
            }
            
            response = await client.post(f"{vllm_url}/v1/chat/completions", json=payload)
            if response.status_code != 200:
                return response.json()
            
            data = response.json()
            choice = data["choices"][0]
            message = choice["message"]
            
            current_messages.append(message)
            
            if message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    result = await execute_tool_call(tool_call)
                    current_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.get("id"),
                        "name": tool_call.get("function", {}).get("name"),
                        "content": json.dumps(result)
                    })
                # Loop back to vLLM with tool results
                continue
            else:
                # Final response (no tool calls)
                return data
