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


def list_running_apps() -> str:
    """List all currently running applications.

    Returns:
        A comma-separated list of running application names
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        # Filter user-visible apps only (not background processes)
        app_names = []
        for app in running_apps:
            name = app.localizedName()
            # activationPolicy() == 0 means regular app (not background)
            if name and app.activationPolicy() == 0:
                app_names.append(name)

        if app_names:
            result = f"Running applications: {', '.join(sorted(app_names))}"
            logger.info("list_running_apps executed", count=len(app_names), success=True)
            return result
        else:
            return "No running applications found"
    except Exception as e:
        error_msg = f"Failed to list running applications: {str(e)}"
        logger.error("list_running_apps failed", error=str(e))
        return error_msg


def is_app_running(appName: str) -> str:
    """Check if a specific application is currently running.

    Args:
        appName: The name of the application to check (e.g., "Spotify", "Chrome")

    Returns:
        A message indicating whether the application is running
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            name = app.localizedName()
            if name and name.lower() == appName.lower():
                logger.info("is_app_running executed", app_name=appName, running=True)
                return f"Yes, '{appName}' is currently running"

        logger.info("is_app_running executed", app_name=appName, running=False)
        return f"No, '{appName}' is not running"
    except Exception as e:
        error_msg = f"Failed to check if '{appName}' is running: {str(e)}"
        logger.error("is_app_running failed", app_name=appName, error=str(e))
        return error_msg


def focus_app(appName: str) -> str:
    """Bring an application to the foreground (same as activate).

    Args:
        appName: The name of the application to focus (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        appscript_app(appName).activate()
        result = f"Application '{appName}' brought to foreground"
        logger.info("focus_app executed", app_name=appName, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to focus '{appName}': {str(e)}"
        logger.error("focus_app failed", app_name=appName, error=str(e))
        return error_msg


def hide_app(appName: str) -> str:
    """Hide a macOS application (keeps it running but invisible).

    Args:
        appName: The name of the application to hide (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            name = app.localizedName()
            if name and name.lower() == appName.lower():
                app.hide()
                result = f"Application '{appName}' hidden successfully"
                logger.info("hide_app executed", app_name=appName, success=True)
                return result

        error_msg = f"Application '{appName}' is not running"
        logger.error("hide_app failed", app_name=appName, error="App not running")
        return error_msg
    except Exception as e:
        error_msg = f"Failed to hide '{appName}': {str(e)}"
        logger.error("hide_app failed", app_name=appName, error=str(e))
        return error_msg


def unhide_app(appName: str) -> str:
    """Unhide (show) a hidden macOS application.

    Args:
        appName: The name of the application to unhide (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            name = app.localizedName()
            if name and name.lower() == appName.lower():
                app.unhide()
                result = f"Application '{appName}' shown successfully"
                logger.info("unhide_app executed", app_name=appName, success=True)
                return result

        error_msg = f"Application '{appName}' is not running"
        logger.error("unhide_app failed", app_name=appName, error="App not running")
        return error_msg
    except Exception as e:
        error_msg = f"Failed to unhide '{appName}': {str(e)}"
        logger.error("unhide_app failed", app_name=appName, error=str(e))
        return error_msg


def restart_app(appName: str) -> str:
    """Restart a macOS application (quit and reopen).

    Args:
        appName: The name of the application to restart (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        # First quit the app
        appscript_app(appName).quit()
        time.sleep(1)  # Wait for app to fully quit

        # Then reopen it
        appscript_app(appName).activate()
        result = f"Application '{appName}' restarted successfully"
        logger.info("restart_app executed", app_name=appName, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to restart '{appName}': {str(e)}"
        logger.error("restart_app failed", app_name=appName, error=str(e))
        return error_msg


def get_app_info(appName: str) -> str:
    """Get information about a macOS application.

    Args:
        appName: The name of the application (e.g., "Spotify", "Chrome")

    Returns:
        Information about the application including bundle ID and status
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        for app in running_apps:
            name = app.localizedName()
            if name and name.lower() == appName.lower():
                bundle_id = app.bundleIdentifier() or "Unknown"
                is_active = app.isActive()
                is_hidden = app.isHidden()

                info = f"Application: {name}\n"
                info += f"Bundle ID: {bundle_id}\n"
                info += f"Status: {'Active (foreground)' if is_active else 'Running in background'}\n"
                info += f"Visibility: {'Hidden' if is_hidden else 'Visible'}"

                logger.info("get_app_info executed", app_name=appName, success=True)
                return info

        error_msg = f"Application '{appName}' is not running or not found"
        logger.error("get_app_info failed", app_name=appName, error="App not found")
        return error_msg
    except Exception as e:
        error_msg = f"Failed to get info for '{appName}': {str(e)}"
        logger.error("get_app_info failed", app_name=appName, error=str(e))
        return error_msg


def launch_app_with_file(appName: str, filePath: str) -> str:
    """Launch an application and open a specific file with it.

    Args:
        appName: The name of the application (e.g., "TextEdit", "Preview")
        filePath: The full path to the file to open (e.g., "/Users/username/document.txt")

    Returns:
        A success message or error description
    """
    try:
        import subprocess
        # Use 'open' command with -a flag for app and file path
        result = subprocess.run(
            ['open', '-a', appName, filePath],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            success_msg = f"Opened '{filePath}' with '{appName}'"
            logger.info("launch_app_with_file executed", app_name=appName, file_path=filePath, success=True)
            return success_msg
        else:
            error_msg = f"Failed to open file: {result.stderr}"
            logger.error("launch_app_with_file failed", app_name=appName, error=result.stderr)
            return error_msg
    except Exception as e:
        error_msg = f"Failed to launch '{appName}' with file '{filePath}': {str(e)}"
        logger.error("launch_app_with_file failed", app_name=appName, file_path=filePath, error=str(e))
        return error_msg


class AppAgent(BaseAgent):
    """Agent for macOS application control"""

    @classmethod
    def get_tool_functions(cls) -> List[callable]:
        """Return list of tool functions for Ollama SDK"""
        return [
            open_app,
            close_app,
            list_running_apps,
            is_app_running,
            focus_app,
            hide_app,
            unhide_app,
            restart_app,
            get_app_info,
            launch_app_with_file,
        ]

    @classmethod
    def get_available_functions(cls) -> Dict[str, callable]:
        """Return dictionary mapping function names to callables"""
        return {
            'open_app': open_app,
            'close_app': close_app,
            'list_running_apps': list_running_apps,
            'is_app_running': is_app_running,
            'focus_app': focus_app,
            'hide_app': hide_app,
            'unhide_app': unhide_app,
            'restart_app': restart_app,
            'get_app_info': get_app_info,
            'launch_app_with_file': launch_app_with_file,
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
