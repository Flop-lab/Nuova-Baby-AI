# Phase 11: Complete Multi-Agent System - Implementation Plan

**Version:** 1.0  
**Date:** November 11, 2025  
**Status:** Draft  
**Prerequisites:** Phase 1-10 (Minimal POC) completed

---

## Table of Contents

1. [Overview](#overview)
2. [Phase 11.1: Complete AppAgent](#phase-111-complete-appagent)
3. [Phase 11.2: BrowserAgent](#phase-112-browseragent)
4. [Phase 11.3: WindowAgent](#phase-113-windowagent)
5. [Phase 11.4: SystemAgent](#phase-114-systemagent)
6. [Phase 11.5: KeyboardAgent](#phase-115-keyboardagent)
7. [Phase 11.6: MouseAgent](#phase-116-mouseagent)
8. [Phase 11.7: ClipboardAgent](#phase-117-clipboardagent)
9. [Phase 11.8: DisplayAgent](#phase-118-displayagent)
10. [Phase 11.9: MediaAgent](#phase-119-mediaagent)
11. [Phase 11.10: FinderAgent](#phase-1110-finderagent)
12. [Final Integration & Testing](#final-integration--testing)

---

## Overview

### Implementation Approach

Each phase follows the same pattern:

1. **Implement Agent** - Add new commands to agent class
2. **Update Tests** - Add unit and integration tests
3. **Manual Testing** - Test via curl against `/api/chat`
4. **Validate** - Ensure no regressions
5. **Commit** - Commit changes before moving to next agent

### Estimated Timeline

**Total:** ~40 hours (1 week)

| Phase | Agent | Time |
|-------|-------|------|
| 11.1 | AppAgent | 4h |
| 11.2 | BrowserAgent | 6h |
| 11.3 | WindowAgent | 4h |
| 11.4 | SystemAgent | 5h |
| 11.5 | KeyboardAgent | 3h |
| 11.6 | MouseAgent | 4h |
| 11.7 | ClipboardAgent | 2h |
| 11.8 | DisplayAgent | 3h |
| 11.9 | MediaAgent | 5h |
| 11.10 | FinderAgent | 4h |

---

## Phase 11.1: Complete AppAgent

**Goal:** Add 8 new commands to AppAgent (already has open_app, close_app from Phase 1-10)

**Time:** 4 hours

### Step 11.1.1: Update AppAgent Implementation

**File:** `src/agents/app_agent.py`

**Add new methods:**

```python
import subprocess
import time
from appscript import app, k

class AppAgent:
    """Agent for macOS application control"""
    
    domain = "app"
    
    # Existing methods from Phase 1-10
    # - open_app(app_name: str)
    # - close_app(app_name: str)
    
    @staticmethod
    async def launch_app(app_name: str) -> dict:
        """Launches an application without activating it"""
        try:
            app(app_name).launch()
            return {"success": True, "result": f"Launched {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def quit_app(app_name: str) -> dict:
        """Gracefully quits an application"""
        try:
            app(app_name).quit()
            return {"success": True, "result": f"Quit {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def force_quit_app(app_name: str) -> dict:
        """Force quits an application (dangerous - requires confirmation)"""
        try:
            result = subprocess.run(['killall', app_name], capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "result": f"Force quit {app_name}"}
            else:
                return {"success": False, "error": f"Failed to force quit {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def hide_app(app_name: str) -> dict:
        """Hides an application"""
        try:
            app('System Events').processes[app_name].visible.set(False)
            return {"success": True, "result": f"Hidden {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def show_app(app_name: str) -> dict:
        """Shows a hidden application"""
        try:
            app('System Events').processes[app_name].visible.set(True)
            return {"success": True, "result": f"Shown {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def is_app_running(app_name: str) -> dict:
        """Checks if an application is currently running"""
        try:
            processes = app('System Events').processes()
            running = any(p.name() == app_name for p in processes)
            return {"success": True, "result": running}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def list_running_apps() -> dict:
        """Lists all currently running applications"""
        try:
            processes = app('System Events').processes()
            # Filter out background-only processes
            apps = [p.name() for p in processes if not p.background_only()]
            return {"success": True, "result": apps}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def get_frontmost_app() -> dict:
        """Gets the name of the frontmost (active) application"""
        try:
            processes = app('System Events').processes()
            frontmost = [p.name() for p in processes if p.frontmost()][0]
            return {"success": True, "result": frontmost}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_tools() -> list:
        """Returns list of all tools this agent provides"""
        return [
            {
                "name": "open_app",
                "description": "Opens and activates a macOS application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "close_app",
                "description": "Closes a macOS application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "launch_app",
                "description": "Launches an application without activating it",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "quit_app",
                "description": "Gracefully quits an application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "force_quit_app",
                "description": "Force quits an application (use only when app is unresponsive)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                },
                "dangerous": True
            },
            {
                "name": "hide_app",
                "description": "Hides an application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "show_app",
                "description": "Shows a hidden application",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "is_app_running",
                "description": "Checks if an application is currently running",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "app_name": {"type": "string", "description": "Name of the application"}
                    },
                    "required": ["app_name"]
                }
            },
            {
                "name": "list_running_apps",
                "description": "Lists all currently running applications",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "get_frontmost_app",
                "description": "Gets the name of the frontmost (active) application",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
        ]
```

### Step 11.1.2: Update Orchestrator Tool Dispatch

**File:** `src/orchestrator/orchestrator.py`

**Update `execute_tool` method to handle new commands:**

```python
async def execute_tool(self, tool_call: dict) -> dict:
    """Executes a tool call and returns the result"""
    tool_name = tool_call.get("name")
    args = tool_call.get("arguments", {})
    
    # AppAgent tools
    if tool_name == "open_app":
        return await AppAgent.open_app(**args)
    elif tool_name == "close_app":
        return await AppAgent.close_app(**args)
    elif tool_name == "launch_app":
        return await AppAgent.launch_app(**args)
    elif tool_name == "quit_app":
        return await AppAgent.quit_app(**args)
    elif tool_name == "force_quit_app":
        # Check if requires confirmation
        if not args.get("confirmed", False):
            return {
                "success": False,
                "requires_confirmation": True,
                "confirmation_message": f"⚠️ Force quit {args['app_name']}? This may cause data loss."
            }
        return await AppAgent.force_quit_app(**args)
    elif tool_name == "hide_app":
        return await AppAgent.hide_app(**args)
    elif tool_name == "show_app":
        return await AppAgent.show_app(**args)
    elif tool_name == "is_app_running":
        return await AppAgent.is_app_running(**args)
    elif tool_name == "list_running_apps":
        return await AppAgent.list_running_apps()
    elif tool_name == "get_frontmost_app":
        return await AppAgent.get_frontmost_app()
    else:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}
```

### Step 11.1.3: Add Unit Tests

**File:** `tests/unit/test_app_agent.py`

```python
import pytest
from unittest.mock import Mock, patch
from src.agents.app_agent import AppAgent

@pytest.mark.asyncio
async def test_launch_app():
    """Test launch_app command"""
    with patch('appscript.app') as mock_app:
        result = await AppAgent.launch_app("TextEdit")
        assert result["success"] == True
        mock_app.assert_called_once_with("TextEdit")

@pytest.mark.asyncio
async def test_quit_app():
    """Test quit_app command"""
    with patch('appscript.app') as mock_app:
        result = await AppAgent.quit_app("TextEdit")
        assert result["success"] == True

@pytest.mark.asyncio
async def test_force_quit_app():
    """Test force_quit_app command"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0)
        result = await AppAgent.force_quit_app("TextEdit")
        assert result["success"] == True
        mock_run.assert_called_once_with(['killall', 'TextEdit'], capture_output=True, text=True)

@pytest.mark.asyncio
async def test_list_running_apps():
    """Test list_running_apps command"""
    with patch('appscript.app') as mock_app:
        mock_process = Mock()
        mock_process.name.return_value = "Safari"
        mock_process.background_only.return_value = False
        mock_app.return_value.processes.return_value = [mock_process]
        
        result = await AppAgent.list_running_apps()
        assert result["success"] == True
        assert "Safari" in result["result"]

@pytest.mark.asyncio
async def test_get_frontmost_app():
    """Test get_frontmost_app command"""
    with patch('appscript.app') as mock_app:
        mock_process = Mock()
        mock_process.name.return_value = "Safari"
        mock_process.frontmost.return_value = True
        mock_app.return_value.processes.return_value = [mock_process]
        
        result = await AppAgent.get_frontmost_app()
        assert result["success"] == True
        assert result["result"] == "Safari"

def test_get_tools():
    """Test that AppAgent returns correct tool definitions"""
    tools = AppAgent.get_tools()
    assert len(tools) == 10  # 2 from Phase 1-10 + 8 new
    tool_names = [t["name"] for t in tools]
    assert "open_app" in tool_names
    assert "launch_app" in tool_names
    assert "force_quit_app" in tool_names
    assert "list_running_apps" in tool_names
```

### Step 11.1.4: Add Integration Tests (macOS only)

**File:** `tests/integration/test_app_agent_integration.py`

```python
import pytest
import sys
from src.agents.app_agent import AppAgent

# Skip all tests if not on macOS
pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="macOS only")

@pytest.mark.asyncio
async def test_launch_and_quit_textedit():
    """Test launching and quitting TextEdit"""
    # Launch TextEdit
    result = await AppAgent.launch_app("TextEdit")
    assert result["success"] == True
    
    # Verify it's running
    result = await AppAgent.is_app_running("TextEdit")
    assert result["success"] == True
    assert result["result"] == True
    
    # Quit TextEdit
    result = await AppAgent.quit_app("TextEdit")
    assert result["success"] == True

@pytest.mark.asyncio
async def test_list_running_apps():
    """Test listing running apps"""
    result = await AppAgent.list_running_apps()
    assert result["success"] == True
    assert isinstance(result["result"], list)
    assert len(result["result"]) > 0  # At least Finder should be running

@pytest.mark.asyncio
async def test_get_frontmost_app():
    """Test getting frontmost app"""
    result = await AppAgent.get_frontmost_app()
    assert result["success"] == True
    assert isinstance(result["result"], str)
    assert len(result["result"]) > 0
```

### Step 11.1.5: Manual Testing with curl

**Start the server:**
```bash
cd baby-ai-python
python -m src.main
```

**Test commands:**

```bash
# Test launch_app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Launch TextEdit without activating it"}'

# Test list_running_apps
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "List all running applications"}'

# Test get_frontmost_app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What app is currently active?"}'

# Test hide_app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hide Safari"}'

# Test is_app_running
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Is Spotify running?"}'
```

### Step 11.1.6: Run Tests

```bash
# Unit tests
pytest tests/unit/test_app_agent.py -v

# Integration tests (macOS only)
pytest tests/integration/test_app_agent_integration.py -v

# All tests
pytest tests/ -v
```

### Step 11.1.7: Commit Changes

```bash
git add src/agents/app_agent.py
git add src/orchestrator/orchestrator.py
git add tests/unit/test_app_agent.py
git add tests/integration/test_app_agent_integration.py
git commit -m "feat(phase-11.1): complete AppAgent with 8 new commands"
git push origin NEWBABY7
```

---

## Phase 11.2: BrowserAgent

**Goal:** Implement BrowserAgent with 15 commands for browser control

**Time:** 6 hours

### Step 11.2.1: Create BrowserAgent

**File:** `src/agents/browser_agent.py`

```python
from appscript import app, k

class BrowserAgent:
    """Agent for web browser control"""
    
    domain = "browser"
    
    @staticmethod
    async def browser_open_url(url: str, browser: str = "Safari") -> dict:
        """Opens a URL in the specified browser"""
        try:
            app(browser).open_location(url)
            return {"success": True, "result": f"Opened {url} in {browser}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_close_tab(browser: str = "Safari") -> dict:
        """Closes the current tab"""
        try:
            app(browser).windows[0].current_tab.close()
            return {"success": True, "result": f"Closed tab in {browser}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_new_tab(url: str, browser: str = "Safari") -> dict:
        """Opens a new tab with the specified URL"""
        try:
            app(browser).windows[0].make(new=k.tab, with_properties={k.URL: url})
            return {"success": True, "result": f"Opened new tab with {url}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_go_back(browser: str = "Safari") -> dict:
        """Navigates back in browser history"""
        try:
            app(browser).windows[0].go_back()
            return {"success": True, "result": "Navigated back"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_go_forward(browser: str = "Safari") -> dict:
        """Navigates forward in browser history"""
        try:
            app(browser).windows[0].go_forward()
            return {"success": True, "result": "Navigated forward"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_reload(browser: str = "Safari") -> dict:
        """Reloads the current page"""
        try:
            app(browser).do_javascript("location.reload()", in_=app(browser).front_document)
            return {"success": True, "result": "Page reloaded"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_get_current_url(browser: str = "Safari") -> dict:
        """Gets the current URL"""
        try:
            url = app(browser).front_document.URL()
            return {"success": True, "result": url}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_get_page_content(browser: str = "Safari") -> dict:
        """Gets the text content of the current page"""
        try:
            content = app(browser).front_document.text()
            return {"success": True, "result": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_scroll_up(browser: str = "Safari", amount: int = 100) -> dict:
        """Scrolls up by the specified amount"""
        try:
            app(browser).do_javascript(f"window.scrollBy(0, -{amount})", in_=app(browser).front_document)
            return {"success": True, "result": f"Scrolled up {amount}px"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_scroll_down(browser: str = "Safari", amount: int = 100) -> dict:
        """Scrolls down by the specified amount"""
        try:
            app(browser).do_javascript(f"window.scrollBy(0, {amount})", in_=app(browser).front_document)
            return {"success": True, "result": f"Scrolled down {amount}px"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_scroll_to_top(browser: str = "Safari") -> dict:
        """Scrolls to the top of the page"""
        try:
            app(browser).do_javascript("window.scrollTo(0, 0)", in_=app(browser).front_document)
            return {"success": True, "result": "Scrolled to top"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_scroll_to_bottom(browser: str = "Safari") -> dict:
        """Scrolls to the bottom of the page"""
        try:
            app(browser).do_javascript("window.scrollTo(0, document.body.scrollHeight)", in_=app(browser).front_document)
            return {"success": True, "result": "Scrolled to bottom"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_find_text(text: str, browser: str = "Safari") -> dict:
        """Finds text on the current page"""
        try:
            result = app(browser).do_javascript(f"window.find('{text}')", in_=app(browser).front_document)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_click_link(text: str, browser: str = "Safari") -> dict:
        """Clicks a link by its text content"""
        try:
            js = f"Array.from(document.querySelectorAll('a')).find(a => a.textContent.includes('{text}'))?.click()"
            app(browser).do_javascript(js, in_=app(browser).front_document)
            return {"success": True, "result": f"Clicked link containing '{text}'"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def browser_switch_tab(index: int, browser: str = "Safari") -> dict:
        """Switches to the tab at the specified index"""
        try:
            app(browser).windows[0].current_tab.set(app(browser).windows[0].tabs[index])
            return {"success": True, "result": f"Switched to tab {index}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_tools() -> list:
        """Returns list of all tools this agent provides"""
        return [
            {
                "name": "browser_open_url",
                "description": "Opens a URL in the specified browser",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "URL to open"},
                        "browser": {"type": "string", "description": "Browser name (Safari, Chrome, Firefox)", "default": "Safari"}
                    },
                    "required": ["url"]
                }
            },
            # ... (add all 15 tool definitions)
        ]
```

### Step 11.2.2: Update Orchestrator

Add BrowserAgent tool dispatch to `src/orchestrator/orchestrator.py`

### Step 11.2.3: Add Tests

Create `tests/unit/test_browser_agent.py` and `tests/integration/test_browser_agent_integration.py`

### Step 11.2.4: Manual Testing

```bash
# Test browser_open_url
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open https://google.com in Safari"}'

# Test browser_get_current_url
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What URL am I on?"}'

# Test browser_scroll_down
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Scroll down the page"}'
```

### Step 11.2.5: Commit

```bash
git add src/agents/browser_agent.py
git add src/orchestrator/orchestrator.py
git add tests/
git commit -m "feat(phase-11.2): add BrowserAgent with 15 commands"
git push origin NEWBABY7
```

---

## Phase 11.3: WindowAgent

**Goal:** Implement WindowAgent with 10 commands for window management

**Time:** 4 hours

### Step 11.3.1: Create WindowAgent

**File:** `src/agents/window_agent.py`

```python
from appscript import app, k
import AppKit

class WindowAgent:
    """Agent for window management"""
    
    domain = "window"
    
    @staticmethod
    def get_screen_size():
        """Gets the main screen size"""
        screen = AppKit.NSScreen.mainScreen()
        frame = screen.frame()
        return int(frame.size.width), int(frame.size.height)
    
    @staticmethod
    async def window_resize(app_name: str, width: int, height: int) -> dict:
        """Resizes the front window"""
        try:
            app(app_name).windows[0].bounds.set([0, 0, width, height])
            return {"success": True, "result": f"Resized {app_name} to {width}x{height}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_move(app_name: str, x: int, y: int) -> dict:
        """Moves the front window"""
        try:
            app(app_name).windows[0].position.set([x, y])
            return {"success": True, "result": f"Moved {app_name} to ({x}, {y})"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_minimize(app_name: str) -> dict:
        """Minimizes the front window"""
        try:
            app(app_name).windows[0].miniaturized.set(True)
            return {"success": True, "result": f"Minimized {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_maximize(app_name: str) -> dict:
        """Maximizes the front window"""
        try:
            width, height = WindowAgent.get_screen_size()
            app(app_name).windows[0].bounds.set([0, 0, width, height])
            return {"success": True, "result": f"Maximized {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_fullscreen(app_name: str) -> dict:
        """Sets the front window to fullscreen"""
        try:
            app('System Events').processes[app_name].windows[0].attributes['AXFullScreen'].value.set(True)
            return {"success": True, "result": f"Set {app_name} to fullscreen"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_tile_left(app_name: str) -> dict:
        """Tiles the window to the left half of the screen"""
        try:
            width, height = WindowAgent.get_screen_size()
            app(app_name).windows[0].bounds.set([0, 0, width // 2, height])
            return {"success": True, "result": f"Tiled {app_name} to left"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_tile_right(app_name: str) -> dict:
        """Tiles the window to the right half of the screen"""
        try:
            width, height = WindowAgent.get_screen_size()
            app(app_name).windows[0].bounds.set([width // 2, 0, width, height])
            return {"success": True, "result": f"Tiled {app_name} to right"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_center(app_name: str) -> dict:
        """Centers the window on the screen"""
        try:
            width, height = WindowAgent.get_screen_size()
            # Center with 50% width and 50% height
            w = width // 2
            h = height // 2
            x = width // 4
            y = height // 4
            app(app_name).windows[0].bounds.set([x, y, x + w, y + h])
            return {"success": True, "result": f"Centered {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_get_bounds(app_name: str) -> dict:
        """Gets the bounds of the front window"""
        try:
            bounds = app(app_name).windows[0].bounds()
            return {"success": True, "result": bounds}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def window_close(app_name: str) -> dict:
        """Closes the front window"""
        try:
            app(app_name).windows[0].close()
            return {"success": True, "result": f"Closed window of {app_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_tools() -> list:
        """Returns list of all tools this agent provides"""
        return [
            # ... (add all 10 tool definitions)
        ]
```

### Step 11.3.2: Add PyObjC Dependency

**File:** `requirements.txt`

Add:
```
pyobjc-framework-Cocoa==12.0
```

### Step 11.3.3-11.3.5: Tests, Manual Testing, Commit

Follow same pattern as Phase 11.1 and 11.2

---

## Phase 11.4: SystemAgent

**Goal:** Implement SystemAgent with 12 commands for file system operations

**Time:** 5 hours

### Step 11.4.1: Create SystemAgent

**File:** `src/agents/system_agent.py`

```python
import os
import shutil
import subprocess
from pathlib import Path

class SystemAgent:
    """Agent for system and file operations"""
    
    domain = "system"
    
    BLOCKED_PATHS = [
        '/System',
        '/Library',
        '/usr',
        '/bin',
        '/sbin',
        '/private',
    ]
    
    @staticmethod
    def is_safe_path(path: str) -> bool:
        """Checks if a path is safe to operate on"""
        abs_path = os.path.abspath(path)
        for blocked in SystemAgent.BLOCKED_PATHS:
            if abs_path.startswith(blocked):
                return False
        return True
    
    @staticmethod
    async def system_read_file(path: str) -> dict:
        """Reads file content"""
        try:
            content = Path(path).read_text()
            return {"success": True, "result": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_write_file(path: str, content: str) -> dict:
        """Writes file content"""
        try:
            if not SystemAgent.is_safe_path(path):
                return {"success": False, "error": f"Cannot write to system path: {path}"}
            
            # Check if file exists and warn
            if Path(path).exists():
                return {
                    "success": False,
                    "requires_confirmation": True,
                    "confirmation_message": f"⚠️ File {path} already exists. Overwrite?"
                }
            
            Path(path).write_text(content)
            return {"success": True, "result": f"Wrote to {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_delete_file(path: str) -> dict:
        """Deletes a file (dangerous - requires confirmation)"""
        try:
            if not SystemAgent.is_safe_path(path):
                return {"success": False, "error": f"Cannot delete system path: {path}"}
            
            Path(path).unlink()
            return {"success": True, "result": f"Deleted {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_copy_file(source: str, destination: str) -> dict:
        """Copies a file"""
        try:
            shutil.copy2(source, destination)
            return {"success": True, "result": f"Copied {source} to {destination}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_move_file(source: str, destination: str) -> dict:
        """Moves a file"""
        try:
            shutil.move(source, destination)
            return {"success": True, "result": f"Moved {source} to {destination}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_download(url: str, destination: str) -> dict:
        """Downloads a file from URL"""
        try:
            result = subprocess.run(['curl', '-L', '-o', destination, url], capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "result": f"Downloaded to {destination}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_list_files(path: str) -> dict:
        """Lists files in a directory"""
        try:
            files = os.listdir(path)
            return {"success": True, "result": files}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_create_directory(path: str) -> dict:
        """Creates a directory"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return {"success": True, "result": f"Created directory {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_delete_directory(path: str) -> dict:
        """Deletes a directory (dangerous - requires confirmation)"""
        try:
            if not SystemAgent.is_safe_path(path):
                return {"success": False, "error": f"Cannot delete system path: {path}"}
            
            shutil.rmtree(path)
            return {"success": True, "result": f"Deleted directory {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_get_file_info(path: str) -> dict:
        """Gets file metadata"""
        try:
            stat = Path(path).stat()
            info = {
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "created": stat.st_ctime,
                "is_file": Path(path).is_file(),
                "is_dir": Path(path).is_dir(),
            }
            return {"success": True, "result": info}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_file_exists(path: str) -> dict:
        """Checks if a file exists"""
        try:
            exists = Path(path).exists()
            return {"success": True, "result": exists}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def system_get_disk_space() -> dict:
        """Gets disk space information"""
        try:
            usage = shutil.disk_usage("/")
            info = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": (usage.used / usage.total) * 100
            }
            return {"success": True, "result": info}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_tools() -> list:
        """Returns list of all tools this agent provides"""
        return [
            # ... (add all 12 tool definitions with dangerous flags)
        ]
```

### Step 11.4.2-11.4.5: Tests, Manual Testing, Commit

Follow same pattern

---

## Phase 11.5-11.10: Remaining Agents

**Follow the same pattern for:**
- Phase 11.5: KeyboardAgent (5 commands, 3 hours)
- Phase 11.6: MouseAgent (8 commands, 4 hours)
- Phase 11.7: ClipboardAgent (4 commands, 2 hours)
- Phase 11.8: DisplayAgent (5 commands, 3 hours)
- Phase 11.9: MediaAgent (15 commands, 5 hours)
- Phase 11.10: FinderAgent (8 commands, 4 hours)

**Each phase:**
1. Create agent file
2. Update orchestrator
3. Add unit tests
4. Add integration tests
5. Manual testing with curl
6. Commit changes

---

## Final Integration & Testing

### Step 12.1: Update Agent Registry

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

AGENTS = [
    AppAgent,
    BrowserAgent,
    WindowAgent,
    SystemAgent,
    KeyboardAgent,
    MouseAgent,
    ClipboardAgent,
    DisplayAgent,
    MediaAgent,
    FinderAgent,
]

def get_all_tools():
    """Collects all tools from all agents"""
    tools = []
    for agent_class in AGENTS:
        tools.extend(agent_class.get_tools())
    return tools
```

### Step 12.2: Update System Prompt

**File:** `src/llm/prompts.py`

Add comprehensive system prompt with:
- All 92 commands documented
- Usage examples for each agent
- Safety warnings
- Multi-agent workflow examples

### Step 12.3: Run Full Test Suite

```bash
# All unit tests
pytest tests/unit/ -v

# All integration tests (macOS only)
pytest tests/integration/ -v

# Coverage report
pytest tests/ --cov=src --cov-report=html
```

### Step 12.4: End-to-End Manual Testing

Test complex multi-agent workflows:

```bash
# Workflow 1: Research and save
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open Google, search for Python tutorials, get the current URL, and save it to a file called tutorials.txt"}'

# Workflow 2: Window management
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open Safari and TextEdit, tile Safari to the left and TextEdit to the right"}'

# Workflow 3: Screenshot and organize
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Take a screenshot, save it to Desktop, then create a folder called Screenshots and move it there"}'
```

### Step 12.5: Final Commit

```bash
git add .
git commit -m "feat(phase-11): complete multi-agent system with 92 commands across 10 agents"
git push origin NEWBABY7
git tag v0.1.0-phase11-complete
git push origin v0.1.0-phase11-complete
```

---

## Success Criteria

Phase 11 is complete when:

✅ All 10 agents implemented (11.1-11.10)  
✅ All 92 commands functional  
✅ Unit tests pass (100% coverage)  
✅ Integration tests pass on macOS  
✅ Manual curl tests successful  
✅ No regressions from Phase 1-10  
✅ Documentation complete  
✅ Safety mechanisms working  
✅ Code committed and tagged  

---

## Troubleshooting

### Common Issues

**1. Accessibility Permissions Denied**
- Grant permissions in System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal (if running from terminal) or Baby AI app

**2. AppleScript Errors**
- Verify app names are correct (case-sensitive)
- Check if app supports AppleScript (use `osascript -e 'tell application "AppName" to get properties'`)

**3. Browser Commands Not Working**
- Safari has best support
- Chrome requires "Allow JavaScript from Apple Events" enabled
- Firefox has limited AppleScript support

**4. Path Permission Errors**
- Check file/directory permissions
- Verify paths are not in BLOCKED_PATHS
- Use absolute paths instead of relative paths

**5. External Tools Missing (ImageMagick, ffmpeg)**
- Install with Homebrew: `brew install imagemagick ffmpeg`
- Or return helpful error message to user

---

**End of Phase 11 Implementation Plan**
