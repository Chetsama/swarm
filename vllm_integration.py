"""
vLLM Integration Module for Swarm Project

This module provides enhanced integration with vLLM infrastructure
for improved routing, tool calling, and LLM capabilities.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
import logging

import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from fastapi import HTTPException
import logging

# Configure logging
logger = logging.getLogger(__name__)

class VLLMIntegration:
    """Handles integration with vLLM infrastructure"""

    def __init__(self, vllm_url: str = "http://vllm:8000", api_prefix: str = "/v1"):
        """
        Initialize vLLM integration

        Args:
            vllm_url: Base URL for vLLM service
            api_prefix: API endpoint prefix
        """
        self.vllm_url = vllm_url
        self.api_prefix = api_prefix
        self.session = None

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def call_vllm_endpoint(self, endpoint: str, payload: Dict[str, Any],
                               method: str = "POST") -> Dict[str, Any]:
        """
        Call a specific vLLM endpoint with proper error handling

        Args:
            endpoint: vLLM endpoint path
            payload: Request payload
            method: HTTP method

        Returns:
            Response from vLLM

        Raises:
            HTTPException: If vLLM call fails
        """
        if not self.session:
            raise HTTPException(status_code=500, detail="vLLM session not initialized")

        url = f"{self.vllm_url}{self.api_prefix}/{endpoint}"

        try:
            async with self.session.request(method, url, json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"vLLM API error: {error_text}"
                    )
        except Exception as e:
            logger.error(f"vLLM call failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to call vLLM: {str(e)}")

    async def get_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from vLLM

        Returns:
            List of model information dictionaries
        """
        try:
            response = await self.call_vllm_endpoint("models", {})
            return response.get("data", [])
        except Exception:
            # Fallback to mock data
            return [
                {
                    "id": "qwen3-coder-30b-4bit",
                    "object": "model",
                    "created": 1700000000,
                    "owned_by": "Swarm"
                }
            ]

    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model

        Args:
            model_name: Name of the model to query

        Returns:
            Model information dictionary
        """
        models = await self.get_models()
        for model in models:
            if model.get("id") == model_name:
                return model
        return {}

    async def chat_completion_with_tools(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform chat completion with tool calling support

        Args:
            payload: Chat completion payload with tools

        Returns:
            Chat completion response
        """
        # Ensure tools are properly formatted for vLLM
        if "tools" in payload and not isinstance(payload["tools"], list):
            payload["tools"] = [payload["tools"]]

        try:
            response = await self.call_vllm_endpoint("chat/completions", payload)
            return response
        except Exception as e:
            logger.error(f"Chat completion failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Chat completion failed: {str(e)}")

class VLLMRoutingManager:
    """Manages routing and coordination with vLLM infrastructure"""

    def __init__(self, vllm_integration: VLLMIntegration):
        """
        Initialize routing manager

        Args:
            vllm_integration: Instance of VLLMIntegration
        """
        self.vllm = vllm_integration
        self.active_routes = {}

    def register_route(self, route_name: str, endpoint: str, method: str = "POST"):
        """
        Register a route for vLLM integration

        Args:
            route_name: Name of the route
            endpoint: vLLM endpoint to route to
            method: HTTP method for the route
        """
        self.active_routes[route_name] = {
            "endpoint": endpoint,
            "method": method
        }

    async def forward_request(self, route_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forward request to registered vLLM route

        Args:
            route_name: Registered route name
            payload: Request payload

        Returns:
            Response from vLLM
        """
        if route_name not in self.active_routes:
            raise HTTPException(status_code=404, detail=f"Route '{route_name}' not found")

        route_config = self.active_routes[route_name]
        return await self.vllm.call_vllm_endpoint(
            route_config["endpoint"],
            payload,
            route_config["method"]
        )

# Global instances for easy access
vllm_integration = None
routing_manager = None

async def initialize_vllm_integration(vllm_url: str = "http://vllm:8000") -> VLLMIntegration:
    """
    Initialize and return vLLM integration instance

    Args:
        vllm_url: URL of the vLLM service

    Returns:
        Initialized VLLMIntegration instance
    """
    global vllm_integration, routing_manager

    if vllm_integration is None:
        vllm_integration = VLLMIntegration(vllm_url)
        routing_manager = VLLMRoutingManager(vllm_integration)

    return vllm_integration

def get_vllm_integration() -> VLLMIntegration:
    """Get the global vLLM integration instance"""
    return vllm_integration

def get_routing_manager() -> VLLMRoutingManager:
    """Get the global routing manager instance"""
    return routing_manager
