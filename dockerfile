FROM vllm/vllm-openai:latest

# Install additional dependencies needed for the swarm
RUN pip install langgraph langchain-core langchain-openai

# Copy the application code
COPY . /app
WORKDIR /app

# Expose ports for the services
EXPOSE 8000 8001 8080 9000 9001

# Default command to run when container starts
CMD ["bash", "-c", "echo 'Swarm service started'"]
