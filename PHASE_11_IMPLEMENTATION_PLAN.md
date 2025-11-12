# Phase 11: Complete Multi-Agent System - Implementation Plan

**Version:** 2.0
**Date:** November 12, 2025
**Status:** Ready for Implementation
**Prerequisites:** Phase 1-10 (Minimal POC) completed

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Decisions](#architecture-decisions)
3. [Phase 11.1: Complete AppAgent](#phase-111-complete-appagent)
4. [Phase 11.2: BrowserAgent](#phase-112-browseragent)
5. [Phase 11.3: WindowAgent](#phase-113-windowagent)
6. [Phase 11.4: SystemAgent](#phase-114-systemagent)
7. [Phase 11.5: KeyboardAgent](#phase-115-keyboardagent)
8. [Phase 11.6: MouseAgent](#phase-116-mouseagent)
9. [Phase 11.7: ClipboardAgent](#phase-117-clipboardagent)
10. [Phase 11.8: DisplayAgent](#phase-118-displayagent)
11. [Phase 11.9: MediaAgent](#phase-119-mediaagent)
12. [Phase 11.10: FinderAgent](#phase-1110-finderagent)
13. [Final Integration & Testing](#final-integration--testing)

---

## Overview

### Implementation Approach

Each phase follows the same pattern:

1. **Implement Agent Commands** - Add new standalone functions to agent file
2. **Update get_tool_functions()** - Register new functions with Ollama SDK
3. **Add Unit Tests** - Test each function individually
4. **Add Integration Tests** - Test via actual macOS APIs (macOS only)
5. **Manual Testing** - Test via Tauri UI or curl against `/api/chat`
6. **Commit** - Commit changes before moving to next agent

### Estimated Timeline

**Total:** ~40 hours (1 week)

| Phase | Agent | Commands | Time |
|-------|-------|----------|------|
| 11.1 | AppAgent | 10 total (2 existing + 8 new) | 4h |
| 11.2 | BrowserAgent | 15 | 6h |
| 11.3 | WindowAgent | 10 | 4h |
| 11.4 | SystemAgent | 12 | 5h |
| 11.5 | KeyboardAgent | 5 | 3h |
| 11.6 | MouseAgent | 8 | 4h |
| 11.7 | ClipboardAgent | 4 | 2h |
| 11.8 | DisplayAgent | 5 | 3h |
| 11.9 | MediaAgent | 15 | 5h |
| 11.10 | FinderAgent | 8 | 4h |

**Total Commands:** 92

---

## Architecture Decisions

### 1. Synchronous Functions (Not Async)

**Current architecture works with synchronous functions:**

```python
def open_app(appName: str) -> str:
    """Open a macOS application by name."""
    try:
        appscript_app(appName).activate()
        return f"Application '{appName}' activated successfully"
    except Exception as e:
        return f"Failed to open '{appName}': {str(e)}"
```

**Rationale:**
- ✅ Works perfectly with Ollama SDK tool calling
- ✅ FastAPI handles async at endpoint level
- ✅ No need for async/await complexity
- ✅ Simpler error handling

### 2. Standalone Functions (Not Static Methods)

**Pattern:**

```python
# ✅ CORRECT (standalone function)
def list_running_apps() -> str:
    """List all currently running applications."""
    # implementation

# ❌ WRONG (static method)
class AppAgent:
    @staticmethod
    def list_running_apps() -> str:
        # implementation
```

**Rationale:**
- ✅ Ollama SDK expects callable functions
- ✅ Simpler to register with `get_tool_functions()`
- ✅ No class instantiation needed

### 3. Ollama SDK Native Tool Calling

**Ollama SDK handles tool dispatch automatically:**

```python
# In orchestrator/orchestrator.py
tools = AppAgent.get_tool_functions()  # Returns [open_app, close_app, ...]
response = ollama_client.chat(
    model="qwen2.5:7b-instruct",
    messages=[...],
    tools=tools  # Ollama automatically calls the right function
)
```

**No manual dispatch needed!** Ollama SDK:
- ✅ Parses LLM tool calls
- ✅ Executes the correct Python function
- ✅ Returns results to LLM
- ✅ Handles errors gracefully

### 4. User Confirmation for Dangerous Commands

**Dangerous commands require user confirmation:**

Commands that:
- Delete files/directories (`system_delete_file`, `system_delete_directory`)
- Force quit apps (`force_quit_app`)
- Modify system settings (`system_set_volume` with extreme values)
- Execute shell commands (`system_execute_command`)

**Implementation Strategy (to be implemented in Phase 11.4):**

```python
def system_delete_file(path: str, confirmed: bool = False) -> str:
    """Delete a file (requires confirmation)."""
    if not confirmed:
        return f"⚠️ CONFIRMATION REQUIRED: Delete file '{path}'? This cannot be undone. Please confirm."

    try:
        os.remove(path)
        return f"File '{path}' deleted successfully"
    except Exception as e:
        return f"Failed to delete '{path}': {str(e)}"
```

**UI will handle confirmation:**
- Tauri frontend shows confirmation dialog
- User clicks "Confirm" or "Cancel"
- If confirmed, command is called again with `confirmed=True`

### 5. Return String (Not Dict)

**All functions return `str` (not `dict`):**

```python
# ✅ CORRECT
def open_app(appName: str) -> str:
    return f"Application '{appName}' activated successfully"

# ❌ WRONG
def open_app(appName: str) -> dict:
    return {"success": True, "result": "..."}
```

**Rationale:**
- ✅ Ollama SDK expects string returns
- ✅ LLM reformulates results naturally
- ✅ Simpler error messages

### 6. Dependencies

**Add to `requirements.txt`:**

```
pyobjc-framework-Cocoa==12.0
pyobjc-framework-Quartz==12.0
```

**External tools (optional, graceful degradation):**
- ImageMagick - for advanced image operations
- ffmpeg - for video/audio conversion

If missing, return helpful error: `"ImageMagick not installed. Install with: brew install imagemagick"`

---

## Phase 11.1: Complete AppAgent

**Goal:** Add 8 new commands to AppAgent (already has `open_app`, `close_app`)

**Time:** 4 hours

**Commands to implement:**
1. ✅ `open_app` - already implemented
2. ✅ `close_app` - already implemented
3. ❌ `list_running_apps` - list all running apps
4. ❌ `is_app_running` - check if app is running
5. ❌ `focus_app` - bring app to foreground
6. ❌ `hide_app` - hide app (keeps running)
7. ❌ `unhide_app` - show hidden app
8. ❌ `restart_app` - quit and reopen app
9. ❌ `get_app_info` - get app info (bundle ID, status)
10. ❌ `launch_app_with_file` - open app with specific file

### Step 11.1.1: Add Dependencies

**File:** `requirements.txt`

Add:
```
pyobjc-framework-Cocoa==12.0
```

Install:
```bash
pip install pyobjc-framework-Cocoa==12.0
```

### Step 11.1.2: Implement New Commands

**File:** `src/agents/app_agent.py`

**Add after `close_app()` function:**

```python
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
```

### Step 11.1.3: Update get_tool_functions()

**File:** `src/agents/app_agent.py`

**Replace the existing `get_tool_functions()` method:**

```python
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
```

### Step 11.1.4: Update System Prompt

**File:** `src/orchestrator/prompts.py`

**Update SYSTEM_PROMPT to document new capabilities:**

```python
SYSTEM_PROMPT = """You are an intelligent macOS automation assistant powered by Baby AI.

**IMPORTANT: Always respond in the same language as the user.**

Your primary role is Function Calling:
1. Analyze the user's request carefully
2. Decide which tools to call (if any) to complete the task
3. After tools execute, you'll receive their results
4. Reformulate the results into natural, friendly language for the user

## Available Tools

### Application Control (10 commands)
- open_app(appName) - Open and activate an application
- close_app(appName) - Close an application
- list_running_apps() - List all running applications
- is_app_running(appName) - Check if an app is running
- focus_app(appName) - Bring app to foreground
- hide_app(appName) - Hide app (keeps running)
- unhide_app(appName) - Show hidden app
- restart_app(appName) - Restart an app
- get_app_info(appName) - Get app details (bundle ID, status)
- launch_app_with_file(appName, filePath) - Open app with specific file

## Examples

User: "What apps are running?"
You: Call list_running_apps(), then say something like "You have Safari, Chrome, and Spotify running."

User: "Is Spotify open?"
You: Call is_app_running("Spotify"), then respond naturally.

User: "Open my document.txt with TextEdit"
You: Call launch_app_with_file("TextEdit", "/path/to/document.txt")

Remember: Be helpful, friendly, and conversational!
"""
```

### Step 11.1.5: Run Tests

```bash
# Install dependencies first
pip install pyobjc-framework-Cocoa==12.0

# Restart backend to load new code
# (Kill existing process and restart)
python -m src.main
```

### Step 11.1.6: Manual Testing

**Test via Tauri UI or curl:**

```bash
# Test 1: List running apps
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What applications are running?"}'

# Test 2: Check if app is running
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is Spotify running?"}'

# Test 3: Hide app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hide Safari"}'

# Test 4: Get app info
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about the Finder app"}'

# Test 5: Restart app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Restart TextEdit"}'
```

### Step 11.1.7: Commit Changes

```bash
git add requirements.txt
git add src/agents/app_agent.py
git add src/orchestrator/prompts.py
git commit -m "feat(phase-11.1): complete AppAgent with 8 new commands

- Add list_running_apps, is_app_running, focus_app
- Add hide_app, unhide_app, restart_app
- Add get_app_info, launch_app_with_file
- Total: 10 AppAgent commands
- Add pyobjc-framework-Cocoa dependency"

git push
```

---

## Phase 11.2: BrowserAgent

**Goal:** Implement BrowserAgent with 15 commands for browser control

**Time:** 6 hours

**Commands to implement:**
1. `browser_open_url(url, browser="Safari")` - Open URL in browser
2. `browser_close_tab(browser="Safari")` - Close current tab
3. `browser_new_tab(url, browser="Safari")` - Open new tab with URL
4. `browser_go_back(browser="Safari")` - Navigate back
5. `browser_go_forward(browser="Safari")` - Navigate forward
6. `browser_reload(browser="Safari")` - Reload page
7. `browser_get_current_url(browser="Safari")` - Get current URL
8. `browser_get_page_title(browser="Safari")` - Get page title
9. `browser_scroll_up(browser="Safari", amount=100)` - Scroll up
10. `browser_scroll_down(browser="Safari", amount=100)` - Scroll down
11. `browser_scroll_to_top(browser="Safari")` - Scroll to top
12. `browser_scroll_to_bottom(browser="Safari")` - Scroll to bottom
13. `browser_find_text(text, browser="Safari")` - Find text on page
14. `browser_click_link(text, browser="Safari")` - Click link by text
15. `browser_switch_tab(index, browser="Safari")` - Switch to tab by index

### Implementation Notes

**Safari support is best.** Chrome requires "Allow JavaScript from Apple Events" enabled. Firefox has limited AppleScript support.

**File:** `src/agents/browser_agent.py`

```python
"""BrowserAgent: Web browser control"""

import structlog
from appscript import app as appscript_app
from typing import List

logger = structlog.get_logger()


def browser_open_url(url: str, browser: str = "Safari") -> str:
    """Open a URL in the specified browser.

    Args:
        url: The URL to open (e.g., "https://google.com")
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        appscript_app(browser).open_location(url)
        result = f"Opened {url} in {browser}"
        logger.info("browser_open_url executed", url=url, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to open URL in {browser}: {str(e)}"
        logger.error("browser_open_url failed", url=url, browser=browser, error=str(e))
        return error_msg


def browser_close_tab(browser: str = "Safari") -> str:
    """Close the current tab in the browser.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        appscript_app(browser).windows[1].current_tab.close()
        result = f"Closed tab in {browser}"
        logger.info("browser_close_tab executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to close tab in {browser}: {str(e)}"
        logger.error("browser_close_tab failed", browser=browser, error=str(e))
        return error_msg


def browser_new_tab(url: str, browser: str = "Safari") -> str:
    """Open a new tab with the specified URL.

    Args:
        url: The URL to open in new tab
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        # For Safari
        if browser.lower() == "safari":
            appscript_app(browser).make(
                new="document",
                with_properties={"URL": url}
            )
        else:
            # For Chrome/Firefox
            appscript_app(browser).open_location(url)

        result = f"Opened new tab with {url} in {browser}"
        logger.info("browser_new_tab executed", url=url, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to open new tab in {browser}: {str(e)}"
        logger.error("browser_new_tab failed", url=url, browser=browser, error=str(e))
        return error_msg


def browser_get_current_url(browser: str = "Safari") -> str:
    """Get the current URL from the active tab.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        The current URL or error description
    """
    try:
        if browser.lower() == "safari":
            url = appscript_app(browser).windows[1].current_tab.URL()
        else:
            url = appscript_app(browser).windows[1].active_tab.URL()

        result = f"Current URL: {url}"
        logger.info("browser_get_current_url executed", browser=browser, url=url, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to get current URL from {browser}: {str(e)}"
        logger.error("browser_get_current_url failed", browser=browser, error=str(e))
        return error_msg


def browser_get_page_title(browser: str = "Safari") -> str:
    """Get the title of the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        The page title or error description
    """
    try:
        if browser.lower() == "safari":
            title = appscript_app(browser).windows[1].current_tab.name()
        else:
            title = appscript_app(browser).windows[1].active_tab.title()

        result = f"Page title: {title}"
        logger.info("browser_get_page_title executed", browser=browser, title=title, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to get page title from {browser}: {str(e)}"
        logger.error("browser_get_page_title failed", browser=browser, error=str(e))
        return error_msg


def browser_reload(browser: str = "Safari") -> str:
    """Reload the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                "location.reload()",
                in_=appscript_app(browser).windows[1].current_tab
            )
        else:
            appscript_app(browser).reload()

        result = f"Reloaded page in {browser}"
        logger.info("browser_reload executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to reload page in {browser}: {str(e)}"
        logger.error("browser_reload failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_down(browser: str = "Safari", amount: int = 300) -> str:
    """Scroll down on the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari
        amount: Pixels to scroll down. Default: 300

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                f"window.scrollBy(0, {amount})",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled down {amount}px in {browser}"
        logger.info("browser_scroll_down executed", browser=browser, amount=amount, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_down failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_up(browser: str = "Safari", amount: int = 300) -> str:
    """Scroll up on the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari
        amount: Pixels to scroll up. Default: 300

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                f"window.scrollBy(0, -{amount})",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled up {amount}px in {browser}"
        logger.info("browser_scroll_up executed", browser=browser, amount=amount, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_up failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_to_top(browser: str = "Safari") -> str:
    """Scroll to the top of the page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                "window.scrollTo(0, 0)",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled to top in {browser}"
        logger.info("browser_scroll_to_top executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_to_top failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_to_bottom(browser: str = "Safari") -> str:
    """Scroll to the bottom of the page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                "window.scrollTo(0, document.body.scrollHeight)",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled to bottom in {browser}"
        logger.info("browser_scroll_to_bottom executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_to_bottom failed", browser=browser, error=str(e))
        return error_msg


def browser_find_text(text: str, browser: str = "Safari") -> str:
    """Find text on the current page.

    Args:
        text: The text to search for
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                f"window.find('{text}')",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Searched for '{text}' in {browser}"
        logger.info("browser_find_text executed", text=text, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to find text in {browser}: {str(e)}"
        logger.error("browser_find_text failed", text=text, browser=browser, error=str(e))
        return error_msg


def browser_click_link(text: str, browser: str = "Safari") -> str:
    """Click a link by its visible text content.

    Args:
        text: The text content of the link to click
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            js_code = f"""
            var links = Array.from(document.querySelectorAll('a'));
            var link = links.find(a => a.textContent.includes('{text}'));
            if (link) {{
                link.click();
                'clicked';
            }} else {{
                'not found';
            }}
            """
            result = appscript_app(browser).do_javascript(
                js_code,
                in_=appscript_app(browser).windows[1].current_tab
            )

            if result == 'clicked':
                msg = f"Clicked link containing '{text}' in {browser}"
                logger.info("browser_click_link executed", text=text, browser=browser, success=True)
                return msg
            else:
                msg = f"Link containing '{text}' not found"
                logger.warning("browser_click_link failed", text=text, browser=browser, error="Link not found")
                return msg
    except Exception as e:
        error_msg = f"Failed to click link in {browser}: {str(e)}"
        logger.error("browser_click_link failed", text=text, browser=browser, error=str(e))
        return error_msg


def browser_go_back(browser: str = "Safari") -> str:
    """Navigate back in browser history.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                "history.back()",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Navigated back in {browser}"
        logger.info("browser_go_back executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to go back in {browser}: {str(e)}"
        logger.error("browser_go_back failed", browser=browser, error=str(e))
        return error_msg


def browser_go_forward(browser: str = "Safari") -> str:
    """Navigate forward in browser history.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_javascript(
                "history.forward()",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Navigated forward in {browser}"
        logger.info("browser_go_forward executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to go forward in {browser}: {str(e)}"
        logger.error("browser_go_forward failed", browser=browser, error=str(e))
        return error_msg


def browser_switch_tab(index: int, browser: str = "Safari") -> str:
    """Switch to a specific tab by index.

    Args:
        index: Tab index (1-based, 1 is first tab)
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).windows[1].current_tab.set(
                appscript_app(browser).windows[1].tabs[index]
            )
            result = f"Switched to tab {index} in {browser}"
            logger.info("browser_switch_tab executed", index=index, browser=browser, success=True)
            return result
        else:
            return f"Tab switching not supported for {browser}. Only Safari is supported."
    except Exception as e:
        error_msg = f"Failed to switch tab in {browser}: {str(e)}"
        logger.error("browser_switch_tab failed", index=index, browser=browser, error=str(e))
        return error_msg


class BrowserAgent:
    """Agent for web browser control"""

    @classmethod
    def get_tool_functions(cls) -> List[callable]:
        """Return list of tool functions for Ollama SDK"""
        return [
            browser_open_url,
            browser_close_tab,
            browser_new_tab,
            browser_get_current_url,
            browser_get_page_title,
            browser_reload,
            browser_scroll_down,
            browser_scroll_up,
            browser_scroll_to_top,
            browser_scroll_to_bottom,
            browser_find_text,
            browser_click_link,
            browser_go_back,
            browser_go_forward,
            browser_switch_tab,
        ]
```

**Follow same testing and commit pattern as Phase 11.1**

---

## Phase 11.3-11.10: Remaining Agents

**NOTE:** Detailed implementation for each agent follows the same pattern as 11.1 and 11.2.

Due to document length, implementation details for remaining agents will be provided upon request or during actual implementation.

### Quick Summary

**Phase 11.3: WindowAgent (10 commands)**
- window_resize, window_move, window_minimize, window_maximize
- window_fullscreen, window_tile_left, window_tile_right
- window_center, window_get_bounds, window_close
- **Dependency:** pyobjc-framework-Quartz

**Phase 11.4: SystemAgent (12 commands)**
- system_read_file, system_write_file, system_delete_file ⚠️
- system_copy_file, system_move_file, system_download
- system_list_files, system_create_directory, system_delete_directory ⚠️
- system_get_file_info, system_file_exists, system_get_disk_space
- **Safety:** Implement confirmation for delete operations

**Phase 11.5: KeyboardAgent (5 commands)**
- keyboard_type_text, keyboard_press_key, keyboard_hotkey
- keyboard_press_and_hold, keyboard_release
- **Uses:** pyautogui or pynput

**Phase 11.6: MouseAgent (8 commands)**
- mouse_move, mouse_click, mouse_double_click
- mouse_right_click, mouse_drag, mouse_scroll
- mouse_get_position, mouse_click_at
- **Uses:** pyautogui or Quartz

**Phase 11.7: ClipboardAgent (4 commands)**
- clipboard_get_text, clipboard_set_text
- clipboard_get_image, clipboard_set_image
- **Uses:** pyperclip and PIL

**Phase 11.8: DisplayAgent (5 commands)**
- display_take_screenshot, display_get_brightness
- display_set_brightness, display_list_displays
- display_get_resolution
- **Uses:** Quartz framework

**Phase 11.9: MediaAgent (15 commands)**
- media_play, media_pause, media_next_track, media_previous_track
- media_get_current_track, media_set_volume, media_get_volume
- media_mute, media_unmute, media_shuffle_on, media_shuffle_off
- media_repeat_on, media_repeat_off, media_seek, media_get_playback_state
- **Target:** Spotify, Music.app via AppleScript

**Phase 11.10: FinderAgent (8 commands)**
- finder_open_folder, finder_reveal_in_finder
- finder_new_folder, finder_select_file
- finder_get_selection, finder_trash_file ⚠️
- finder_empty_trash ⚠️, finder_get_info
- **Safety:** Implement confirmation for trash operations

---

## Final Integration & Testing

### Update Orchestrator

**File:** `src/orchestrator/orchestrator.py`

```python
from src.agents.app_agent import AppAgent
from src.agents.browser_agent import BrowserAgent
from src.agents.window_agent import WindowAgent
from src.agents.system_agent import SystemAgent
from src.agents.keyboard_agent import KeyboardAgent
from src.agents.mouse_agent import MouseAgent
from src.agents.clipboard_agent import ClipboardAgent
from src.agents.display_agent import DisplayAgent
from src.agents.media_agent import MediaAgent
from src.agents.finder_agent import FinderAgent

def get_all_tools():
    """Collect all tools from all agents"""
    all_tools = []

    all_tools.extend(AppAgent.get_tool_functions())
    all_tools.extend(BrowserAgent.get_tool_functions())
    all_tools.extend(WindowAgent.get_tool_functions())
    all_tools.extend(SystemAgent.get_tool_functions())
    all_tools.extend(KeyboardAgent.get_tool_functions())
    all_tools.extend(MouseAgent.get_tool_functions())
    all_tools.extend(ClipboardAgent.get_tool_functions())
    all_tools.extend(DisplayAgent.get_tool_functions())
    all_tools.extend(MediaAgent.get_tool_functions())
    all_tools.extend(FinderAgent.get_tool_functions())

    return all_tools
```

### Update System Prompt

**File:** `src/orchestrator/prompts.py`

Add comprehensive documentation for all 92 commands.

### End-to-End Testing

**Complex multi-agent workflows:**

```bash
# Workflow 1: Research and save
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open Google, search for Python tutorials, and save the URL to tutorials.txt"}'

# Workflow 2: Window management
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open Safari and TextEdit, tile Safari to the left and TextEdit to the right"}'

# Workflow 3: Screenshot and organize
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Take a screenshot, save it to Desktop, create a Screenshots folder, and move it there"}'
```

### Final Commit

```bash
git add .
git commit -m "feat(phase-11): complete multi-agent system with 92 commands

- Implement 10 agents: App, Browser, Window, System, Keyboard, Mouse, Clipboard, Display, Media, Finder
- Total: 92 commands
- Add user confirmation for dangerous operations
- Update system prompt with all capabilities
- Add comprehensive tests"

git push
git tag v0.2.0-phase11-complete
git push --tags
```

---

## Success Criteria

Phase 11 is complete when:

✅ All 10 agents implemented
✅ All 92 commands functional
✅ Ollama SDK tool calling works for all commands
✅ Confirmation system works for dangerous operations
✅ Manual testing successful via Tauri UI
✅ No regressions from Phase 1-10
✅ System prompt documents all capabilities
✅ Code committed and tagged

---

## Troubleshooting

### Accessibility Permissions

**Error:** "Accessibility permissions denied"

**Fix:** Grant permissions in System Preferences → Security & Privacy → Privacy → Accessibility. Add Baby AI app or Terminal.

### AppleScript Errors

**Error:** "Application not found" or "Command failed"

**Fix:**
- Verify app name is correct (case-sensitive)
- Check if app supports AppleScript: `osascript -e 'tell application "AppName" to get properties'`

### Browser Commands Not Working

**Safari:** Works best, full support
**Chrome:** Requires "Allow JavaScript from Apple Events" in View → Developer
**Firefox:** Limited AppleScript support, some commands may not work

### PyObjC Import Errors

**Error:** "No module named 'AppKit'"

**Fix:** `pip install pyobjc-framework-Cocoa==12.0`

### External Tools Missing

**ImageMagick or ffmpeg not found**

**Fix:** `brew install imagemagick ffmpeg`

Or return helpful error to user: "ImageMagick not installed. Install with: brew install imagemagick"

---

**End of Phase 11 Implementation Plan v2.0**
