import importlib
import inspect
import os
from typing import Dict, List
from langchain.tools import BaseTool, tool

def get_tools_from_module(module_path: str) -> List[BaseTool]:
    """Dynamically imports a module and extracts all functions decorated with @tool."""
    tools = []
    # Convert file path to module path (e.g., tools/filesystem.py -> tools.filesystem)
    module_name = module_path.replace("/", ".").replace(".py", "")
    
    try:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, "name") and hasattr(obj, "description") and isinstance(obj, BaseTool):
                tools.append(obj)
    except Exception as e:
        print(f"Error loading tools from {module_path}: {e}")
        
    return tools

def load_all_tools(tools_dir: str = "tools") -> List[BaseTool]:
    """Scans the tools directory and loads all decorated tools."""
    all_tools = []
    for entry in os.scandir(tools_dir):
        if entry.is_file() and entry.name.endswith(".py") and entry.name != "__init__.py" and entry.name != "registry.py":
            all_tools.extend(get_tools_from_module(f"{tools_dir}/{entry.name}"))
    return all_tools

def get_tools_map(tools: List[BaseTool]) -> Dict[str, BaseTool]:
    """Returns a dictionary mapping tool names to tool objects."""
    return {t.name: t for t in tools}
