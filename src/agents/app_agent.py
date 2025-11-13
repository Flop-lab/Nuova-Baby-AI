import time
import uuid
from typing import List, Dict, Any
from appscript import app as appscript_app
from src.agents.base import BaseAgent
from src.models.schemas import ToolCall, ExecutionResult
import structlog

logger = structlog.get_logger()

# Tool functions for Ollama (exposed as Python functions with proper docstrings)
def open_app(appName: str) -> str:
    """Open a macOS application by name.

    Args:
        appName: The name of the application to open (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        appscript_app(appName).activate()
        result = f"Application '{appName}' activated successfully"
        logger.info("open_app executed", app_name=appName, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to open '{appName}': {str(e)}"
        logger.error("open_app failed", app_name=appName, error=str(e))
        return error_msg


def close_app(appName: str) -> str:
    """Close a macOS application by name.

    Args:
        appName: The name of the application to close (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        appscript_app(appName).quit()
        result = f"Application '{appName}' closed successfully"
        logger.info("close_app executed", app_name=appName, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to close '{appName}': {str(e)}"
        logger.error("close_app failed", app_name=appName, error=str(e))
        return error_msg


class AppAgent(BaseAgent):
    """Agent for macOS application control"""

    @classmethod
    def get_tool_functions(cls) -> List[callable]:
        """Return list of tool functions for Ollama SDK"""
        return [open_app, close_app]

    @classmethod
    def get_available_functions(cls) -> Dict[str, callable]:
        """Return dictionary mapping function names to callables"""
        return {
            'open_app': open_app,
            'close_app': close_app,
        }

    @classmethod
    def get_tools(cls) -> List[Dict[str, Any]]:
        """Legacy method - returns tool definitions as dicts"""
        return [
            {
                "name": "open_app",
                "description": "Open a macOS application by name.",
                "parameters": {
                    "appName": {"type": "string", "description": "Name of the application to open."},
                },
                "required": ["appName"],
            },
            {
                "name": "close_app",
                "description": "Close a macOS application by name.",
                "parameters": {
                    "appName": {"type": "string", "description": "Name of the application to close."},
                },
                "required": ["appName"],
            },
        ]

    def execute(self, tool_call: ToolCall) -> ExecutionResult:
        """Legacy execute method - kept for backward compatibility"""
        start = time.time()
        func = tool_call.function.name
        app_name = tool_call.function.arguments.get("appName")

        if not app_name:
            output = None
            success = False
            error = "Missing required argument: appName"
        elif func == "open_app":
            result_str = open_app(app_name)
            success = "successfully" in result_str
            output = result_str if success else None
            error = None if success else result_str
        elif func == "close_app":
            result_str = close_app(app_name)
            success = "successfully" in result_str
            output = result_str if success else None
            error = None if success else result_str
        else:
            output = None
            success = False
            error = f"Unknown function: {func}"

        duration_ms = (time.time() - start) * 1000
        return ExecutionResult(success=success, output=output, error=error, duration_ms=duration_ms)
