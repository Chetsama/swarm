import subprocess
from langchain.tools import tool

@tool
def git_status() -> str:
    """Returns the output of 'git status'."""
    result = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True
    )
    return result.stdout

@tool
def git_diff() -> str:
    """Returns the output of 'git diff'."""
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True
    )
    return result.stdout
