FROM vllm/vllm-openai:latest

# Install git (required for pip git installs)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install FlashInfer
RUN pip install --upgrade \
    git+https://github.com/huggingface/transformers.git \
    git+https://github.com/vllm-project/vllm.git
