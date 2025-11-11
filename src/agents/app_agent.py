import time
import uuid
from typing import List, Dict, Any
from appscript import app as appscript_app
from src.agents.base import BaseAgent
from src.models.schemas import ToolCall, ExecutionResult
import structlog

logger = structlog.get_logger()

class AppAgent(BaseAgent):
    """Agent for macOS application control"""
    @classmethod
    def get_tools(cls) -> List[Dict[str, Any]]:
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
        start = time.time()
        try:
            func = tool_call.function.name
            app_name = tool_call.function.arguments.get("appName")
            if func == "open_app":
                appscript_app(app_name).activate()
                output = f"Application '{app_name}' activated successfully"
                success = True
                error = None
            elif func == "close_app":
                appscript_app(app_name).quit()
                output = f"Application '{app_name}' closed successfully"
                success = True
                error = None
            else:
                output = None
                success = False
                error = f"Unknown function: {func}"
        except Exception as e:
            output = None
            success = False
            error = str(e)
        duration_ms = (time.time() - start) * 1000
        logger.info("AppAgent execution", function=func, app_name=app_name, success=success, error=error)
        return ExecutionResult(success=success, output=output, error=error, duration_ms=duration_ms)
