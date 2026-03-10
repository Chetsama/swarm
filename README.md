<h1>Swarm</h1>

Project Structure
```
  ai-dev-cloud/
  ├─ docker-compose.yml
  ├─ gateway/
  │   └─ fastapi_router.py
  ├─ agents/
  │   ├─ planner.py
  │   ├─ executor.py
  │   └─ critic.py
  ├─ rag/
  │   └─ retriever.py
  ├─ tools/
  │   ├─ shell.py
  │   ├─ filesystem.py
  │   └─ git.py
  └─ models/
```

Ran into permissions issue with docker

```
  unable to get image 'chromadb/chroma': permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.51/images/chromadb/chroma/json": dial unix /var/run/docker.sock: connect: permission denied
```
Had to run
```
  sudo chmod 777 /var/run/docker.sock
```

Nvidia runtime issue

https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam/issues/132#issuecomment-2134831510

curl http://gateway.coffee-dev.uk/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model":"qwen3-coder",
    "messages":[{"role":"user","content":"write a hello world in go"}]
  }'


Things to try
--chunked-prefill
--prefix-cache
--dtype float16
--use-cuda-graph

On a single 3090, increasing max-num-batched-tokens slightly (e.g., 512–768) may increase throughput without hitting VRAM limits, especially if you combine it with explicit KV cache allocation.

Give exact number of cpu threads
export OMP_NUM_THREADS=8
