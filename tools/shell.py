import subprocess
from langchain.tools import tool

@tool
def run_shell_command(cmd: str) -> str:
    """Executes a shell command and returns the stdout and stderr."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nRETURN CODE: {result.returncode}"

    except Exception as e:
        return f"Error: {str(e)}"
