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
  chmod 777 /var/run/docker.sock
```

Nvidia runtime issue

https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_visual_slam/issues/132#issuecomment-2134831510

curl http://gateway.coffee-dev.uk/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "model":"deepseek-coder",
    "messages":[{"role":"user","content":"write a hello world in go"}]
  }'
