Can you please attempt a minimal implementation of langgraph?

Currently, a message is sent to http://localhost:9000, this is then proxied to vLLM via the gateway/fastapi_router.py. I would like to maintain this flow, but add in a langgraph service so the new flow would look like

http://localhost:9000 -> fastapi_router.py -> langgraph agent orchestrator -> vLLM

For this first pass I would like you to do the following.

Create a minimal langgraph implementation with a single planner agent and point it towards vLLM running at http://vllm:8000. Please see this documentation on how to do that https://docs.langchain.com/oss/python/integrations/chat/vllm

Adjust the docker compose and gateway/fastapi_router.py to maintain the current flow.

Favour editing existing files over creating new ones. Don't attempt to run the project. Please don't delete any existing files. If you are unsure about anything ask me
