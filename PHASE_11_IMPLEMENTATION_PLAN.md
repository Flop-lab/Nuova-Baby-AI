# Phase 11: Multi-Agent System with Pydantic AI - Implementation Plan

**Version:** 3.2 - Pydantic AI Edition (NATIVE macOS APIs)
**Date:** November 14, 2025
**Status:** ✅ Ready for Implementation
**Prerequisites:**
- ✅ Phase 10.1 (Pydantic AI Integration) completed
- ✅ Pydantic AI 1.14.0 installed and working
- ✅ Current tools: `open_app`, `close_app`
- **Official Docs:** https://ai.pydantic.dev

---

## 🔄 What Changed from v3.1 → v3.2

**v3.2 uses ONLY native macOS APIs - professional approach:**

### Major Changes:
1. ✅ **Removed pyautogui** - using native CGEvent APIs instead (Quartz framework)
2. ✅ **Removed pynput** - redundant with CGEvent
3. ✅ **Removed pyperclip usage** - using native NSPasteboard instead (better for text + images)
4. ✅ **Kept Pillow** - necessary for image handling
5. ✅ **Only 2 new dependencies** instead of 4:
   - pyobjc-framework-Quartz==12.0 (for display, mouse, keyboard)
   - Pillow==12.0.0 (for images)
6. ✅ **Better macOS integration** - native permissions, better performance, more professional

### Why Native APIs?
- **Better permissions handling**: macOS native frameworks require proper permissions
- **Better performance**: No cross-platform overhead
- **More features**: NSPasteboard handles text AND images, CGEvent has full keyboard/mouse control
- **Professional code**: Using Apple frameworks directly is best practice on macOS
- **Less dependencies**: 2 packages instead of 4

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture with Pydantic AI](#architecture-with-pydantic-ai)
3. [Complete Dependencies (All Phases)](#complete-dependencies-all-phases)
4. [Phase 11.1: Complete AppAgent Tools](#phase-111-complete-appagent-tools)
5. [Phase 11.2: Browser Tools](#phase-112-browser-tools)
6. [Phase 11.3-11.10: Remaining Tool Categories](#phase-113-1110-remaining-tool-categories)
7. [Testing & Validation](#testing--validation)

---

## Overview

### What We're Building

**Goal:** Add 82 tools to the existing Pydantic AI agent incrementally (total: 84 tools).

**Current State:**
- ✅ `src/agents/pydantic_agent.py` with 2 tools: `open_app`, `close_app`
- ✅ Pydantic AI working with Ollama
- ✅ Frontend integrated and tested

**Target State:**
- 84 total tools across 10 categories
- All tools registered with `@agent.tool` decorator
- Single unified agent (no multiple agent classes)
- Comprehensive system prompt documentation
- **NO dangerous operations** (delete, trash) - moved to future Phase 11.11

### Implementation Strategy

**Incremental Approach:**
1. Add 8-10 tools per phase
2. Update system prompt after each phase
3. Test thoroughly before moving to next phase
4. Commit after each phase completion

**Time Estimate:** ~30-40 hours (1 week)

---

## Architecture with Pydantic AI

### Pattern: @agent.tool Decorator

**This is the ONLY way to register tools in Pydantic AI:**

```python
# src/agents/pydantic_agent.py

@agent.tool
def list_running_apps(ctx: RunContext) -> str:
    """List all currently running applications.

    Returns:
        A comma-separated list of running application names
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        app_names = []
        for app in running_apps:
            name = app.localizedName()
            if name and app.activationPolicy() == 0:  # Regular apps only
                app_names.append(name)

        return f"Running applications: {', '.join(sorted(app_names))}"
    except Exception as e:
        logger.error("list_running_apps_failed", error=str(e))
        return f"Failed to list running applications: {str(e)}"
```

### Key Principles

1. **No Classes Required**
   - Just functions with `@agent.tool` decorator
   - No `BaseAgent`, `AppAgent`, etc.

2. **RunContext First Parameter**
   - All tools must have `ctx: RunContext` as first param
   - Enables dependency injection (not used now, but required by Pydantic AI)

3. **Docstrings Are Critical**
   - Pydantic AI extracts docstrings and sends them to LLM
   - LLM uses docstrings to decide when to call tools
   - Format: Brief description + Args + Returns sections

4. **Return Strings**
   - All tools return `str` (not `dict` or Pydantic models)
   - LLM reformulates results naturally

5. **Single Agent Instance**
   - One global `agent` variable in `pydantic_agent.py`
   - All tools registered to same agent
   - No need for tool collection or merging

### File Structure

```
src/agents/
└── pydantic_agent.py    # ← Single file with ALL tools (target: 84 tools)
```

**No other agent files needed!**

---

## Complete Dependencies (All Phases)

### Required Python Packages - NATIVE APPROACH

**🎯 Only 2 new dependencies needed!**

```bash
cd "/Users/alessandro/Nuova Baby AI"
source venv/bin/activate

# Phase 11.8, 11.5, 11.6: Display, Keyboard, Mouse (native CGEvent APIs)
pip install pyobjc-framework-Quartz==12.0

# Phase 11.7: Clipboard and Screenshot image handling
pip install Pillow==12.0.0
```

**Update `requirements.txt`:**

Add these lines at the end of `requirements.txt`:

```txt
# Phase 11: Multi-Agent System - Native macOS Dependencies
# macOS Quartz Framework (Phase 11.5, 11.6, 11.8)
pyobjc-framework-Quartz==12.0  # Display, keyboard, mouse via CGEvent

# Image handling (Phase 11.7, 11.8)
Pillow==12.0.0                 # Screenshots and clipboard images

# NOTES:
# - Phase 11.1, 11.3, 11.9, 11.10: Use pyobjc-framework-Cocoa (ALREADY INSTALLED)
# - Phase 11.2, 11.4: Use only built-in Python libraries
# - Phase 11.7: Uses NSPasteboard (in Cocoa, already installed) + Pillow
# - pyperclip is already in requirements.txt but WON'T be used (NSPasteboard is better)
```

### Already Installed (No Action Needed)

These packages are ALREADY in `requirements.txt` and will be used:

```txt
appscript==1.4.0                # For AppleScript (browser, media, finder)
pyobjc-core==12.0               # PyObjC base (already installed)
pyobjc-framework-Cocoa==12.0    # AppKit, NSWorkspace, NSPasteboard (already installed)
pyperclip==1.11.0               # Already installed but WON'T be used (we use NSPasteboard)
```

### Dependency Verification

**After installation, verify packages:**

```bash
pip list | grep -E "pyobjc-framework|Pillow"

# Expected output:
# Pillow                      12.0.0
# pyobjc-core                 12.0      (already installed)
# pyobjc-framework-Cocoa      12.0      (already installed)
# pyobjc-framework-Quartz     12.0      (NEW)
```

### macOS Compatibility

- ✅ **PyObjC 12.0**: Compatible with macOS Sequoia (15.x) and earlier
- ✅ **Pillow 12.0.0**: Latest (October 2025) - macOS universal binary
- ✅ **Native CGEvent**: Works on macOS 10.5+ (all modern macOS versions)
- ✅ **NSPasteboard**: Built into macOS (AppKit framework)

### Why This Approach?

**vs. pyautogui:**
- ✅ Native CGEvent has full keyboard/mouse control
- ✅ Better macOS permissions integration
- ✅ No cross-platform overhead

**vs. pynput:**
- ✅ Redundant with CGEvent
- ✅ CGEvent is the native macOS API that pynput uses internally

**vs. pyperclip:**
- ✅ NSPasteboard handles TEXT + IMAGES (pyperclip only text)
- ✅ Native macOS clipboard API
- ✅ Better integration with macOS apps
- ✅ Already available (Cocoa framework installed)

---

## Phase 11.1: Complete AppAgent Tools

**Goal:** Add 8 new app control tools (currently have 2)

**Time:** 4 hours

**New Tools to Add:**
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

### Step 11.1.1: Install Dependencies

**Note:** Phase 11.1 only needs Cocoa (already installed). Quartz will be installed later.

```bash
cd "/Users/alessandro/Nuova Baby AI"
source venv/bin/activate

# Check if Cocoa is already installed
pip list | grep pyobjc-framework-Cocoa

# If not installed (should be):
pip install pyobjc-framework-Cocoa==12.0
```

### Step 11.1.2: Add Imports to pydantic_agent.py

**File:** `src/agents/pydantic_agent.py`

**IMPORTANT:** Add these imports at the TOP of the file, after the existing imports.

**Current imports (lines 8-19):**
```python
import os
import uuid
import json
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from appscript import app as appscript_app
import structlog

from src.models.schemas import ChatResponse, ChatChunk
from src.orchestrator.prompts import SYSTEM_PROMPT
```

**Add these NEW imports after line 11 (`from appscript import app as appscript_app`):**

```python
import time           # For restart_app delays
import subprocess     # For launch_app_with_file
```

**Final import block should look like:**

```python
import os
import uuid
import json
import time           # NEW: For restart_app delays
import subprocess     # NEW: For launch_app_with_file
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from appscript import app as appscript_app
import structlog

from src.models.schemas import ChatResponse, ChatChunk
from src.orchestrator.prompts import SYSTEM_PROMPT
```

### Step 11.1.3: Add New Tools to pydantic_agent.py

**File:** `src/agents/pydantic_agent.py`

**Add after the existing `close_app` function:**

```python
@agent.tool
def list_running_apps(ctx: RunContext) -> str:
    """List all currently running applications.

    Returns:
        A comma-separated list of running application names
    """
    try:
        from AppKit import NSWorkspace
        workspace = NSWorkspace.sharedWorkspace()
        running_apps = workspace.runningApplications()

        app_names = []
        for app in running_apps:
            name = app.localizedName()
            if name and app.activationPolicy() == 0:
                app_names.append(name)

        if app_names:
            result = f"Running applications: {', '.join(sorted(app_names))}"
            logger.info("list_running_apps_executed", count=len(app_names))
            return result
        else:
            return "No running applications found"
    except Exception as e:
        logger.error("list_running_apps_failed", error=str(e))
        return f"Failed to list running applications: {str(e)}"


@agent.tool
def is_app_running(ctx: RunContext, appName: str) -> str:
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
                logger.info("is_app_running_executed", app_name=appName, running=True)
                return f"Yes, '{appName}' is currently running"

        logger.info("is_app_running_executed", app_name=appName, running=False)
        return f"No, '{appName}' is not running"
    except Exception as e:
        logger.error("is_app_running_failed", app_name=appName, error=str(e))
        return f"Failed to check if '{appName}' is running: {str(e)}"


@agent.tool
def focus_app(ctx: RunContext, appName: str) -> str:
    """Bring an application to the foreground (same as activate).

    Args:
        appName: The name of the application to focus (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        appscript_app(appName).activate()
        logger.info("focus_app_executed", app_name=appName)
        return f"Application '{appName}' brought to foreground"
    except Exception as e:
        logger.error("focus_app_failed", app_name=appName, error=str(e))
        return f"Failed to focus '{appName}': {str(e)}"


@agent.tool
def hide_app(ctx: RunContext, appName: str) -> str:
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
                logger.info("hide_app_executed", app_name=appName)
                return f"Application '{appName}' hidden successfully"

        logger.error("hide_app_failed", app_name=appName, error="App not running")
        return f"Application '{appName}' is not running"
    except Exception as e:
        logger.error("hide_app_failed", app_name=appName, error=str(e))
        return f"Failed to hide '{appName}': {str(e)}"


@agent.tool
def unhide_app(ctx: RunContext, appName: str) -> str:
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
                logger.info("unhide_app_executed", app_name=appName)
                return f"Application '{appName}' shown successfully"

        logger.error("unhide_app_failed", app_name=appName, error="App not running")
        return f"Application '{appName}' is not running"
    except Exception as e:
        logger.error("unhide_app_failed", app_name=appName, error=str(e))
        return f"Failed to unhide '{appName}': {str(e)}"


@agent.tool
def restart_app(ctx: RunContext, appName: str) -> str:
    """Restart a macOS application (quit and reopen).

    Args:
        appName: The name of the application to restart (e.g., "Spotify", "Chrome")

    Returns:
        A success message or error description
    """
    try:
        appscript_app(appName).quit()
        time.sleep(1)
        appscript_app(appName).activate()
        logger.info("restart_app_executed", app_name=appName)
        return f"Application '{appName}' restarted successfully"
    except Exception as e:
        logger.error("restart_app_failed", app_name=appName, error=str(e))
        return f"Failed to restart '{appName}': {str(e)}"


@agent.tool
def get_app_info(ctx: RunContext, appName: str) -> str:
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

                logger.info("get_app_info_executed", app_name=appName)
                return info

        logger.error("get_app_info_failed", app_name=appName, error="App not found")
        return f"Application '{appName}' is not running or not found"
    except Exception as e:
        logger.error("get_app_info_failed", app_name=appName, error=str(e))
        return f"Failed to get info for '{appName}': {str(e)}"


@agent.tool
def launch_app_with_file(ctx: RunContext, appName: str, filePath: str) -> str:
    """Launch an application and open a specific file with it.

    Args:
        appName: The name of the application (e.g., "TextEdit", "Preview")
        filePath: The full path to the file to open (e.g., "/Users/username/document.txt")

    Returns:
        A success message or error description
    """
    try:
        result = subprocess.run(
            ['open', '-a', appName, filePath],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            logger.info("launch_app_with_file_executed", app_name=appName, file_path=filePath)
            return f"Opened '{filePath}' with '{appName}'"
        else:
            logger.error("launch_app_with_file_failed", app_name=appName, error=result.stderr)
            return f"Failed to open file: {result.stderr}"
    except Exception as e:
        logger.error("launch_app_with_file_failed", app_name=appName, file_path=filePath, error=str(e))
        return f"Failed to launch '{appName}' with file '{filePath}': {str(e)}"
```

### Step 11.1.4: Update System Prompt

**File:** `src/orchestrator/prompts.py`

Update the `SYSTEM_PROMPT` to document new capabilities:

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

User: "Hide Safari"
You: Call hide_app("Safari"), then confirm.

User: "Tell me about Finder"
You: Call get_app_info("Finder"), then present the information nicely.

Remember: Be helpful, friendly, and conversational!
"""
```

### Step 11.1.5: Test New Tools

```bash
# Restart backend
cd "/Users/alessandro/Nuova Baby AI"
source venv/bin/activate
python -m src.main
```

**Test via curl:**

```bash
# Test 1: List running apps
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quali applicazioni sono in esecuzione?", "stream": false}'

# Test 2: Check if app is running
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Spotify è aperto?", "stream": false}'

# Test 3: Hide app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Nascondi Safari", "stream": false}'

# Test 4: Get app info
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Dimmi informazioni su Finder", "stream": false}'

# Test 5: Restart app
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Riavvia TextEdit", "stream": false}'
```

**Verify tool execution in logs:**

```bash
# Check that tools were actually called
tail -f /tmp/baby-ai-backend.log | grep -E "tool:|running tool:"
```

### Step 11.1.6: Commit Phase 11.1

```bash
git add requirements.txt
git add src/agents/pydantic_agent.py
git add src/orchestrator/prompts.py
git commit -m "$(cat <<'EOF'
feat: Phase 11.1 - Complete AppAgent with 8 new tools

Add comprehensive app control capabilities to Pydantic AI agent:
- list_running_apps: List all running applications
- is_app_running: Check if specific app is running
- focus_app: Bring app to foreground
- hide_app: Hide app (keeps running)
- unhide_app: Show hidden app
- restart_app: Quit and reopen app
- get_app_info: Get app bundle ID and status
- launch_app_with_file: Open app with specific file

Technical:
- All tools use @agent.tool decorator (Pydantic AI pattern)
- Add pyobjc-framework-Cocoa==12.0 dependency
- Add time and subprocess imports at top of file
- Update system prompt with 10 app control commands
- Total: 10 app control tools working

Testing: ✅ All 8 new tools tested with curl

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Phase 11.2: Browser Tools

**Goal:** Add 15 browser automation tools

**Time:** 6 hours

**Tools to Add:**
1. `browser_open_url(url, browser="Safari")` - Open URL in browser
2. `browser_close_tab(browser="Safari")` - Close current tab
3. `browser_new_tab(url, browser="Safari")` - Open new tab with URL
4. `browser_go_back(browser="Safari")` - Navigate back
5. `browser_go_forward(browser="Safari")` - Navigate forward
6. `browser_reload(browser="Safari")` - Reload current page
7. `browser_get_current_url(browser="Safari")` - Get current URL
8. `browser_get_page_title(browser="Safari")` - Get page title
9. `browser_scroll_up(browser="Safari", amount=100)` - Scroll up
10. `browser_scroll_down(browser="Safari", amount=100)` - Scroll down
11. `browser_scroll_to_top(browser="Safari")` - Scroll to top
12. `browser_scroll_to_bottom(browser="Safari")` - Scroll to bottom
13. `browser_find_text(text, browser="Safari")` - Find text on page
14. `browser_click_link(text, browser="Safari")` - Click link by text
15. `browser_switch_tab(index, browser="Safari")` - Switch to tab by index

**Dependencies:** Built-in AppleScript via `appscript` (already installed)

**Implementation Pattern:**

```python
@agent.tool
def browser_open_url(ctx: RunContext, url: str, browser: str = "Safari") -> str:
    """Open a URL in the specified browser.

    Args:
        url: The URL to open (e.g., "https://google.com")
        browser: Browser name (default: "Safari", also supports "Chrome", "Firefox")

    Returns:
        Success message or error description
    """
    try:
        # AppleScript command via appscript
        browser_app = appscript_app(browser)
        browser_app.open_location(url)
        logger.info("browser_open_url_executed", url=url, browser=browser)
        return f"Opened '{url}' in {browser}"
    except Exception as e:
        logger.error("browser_open_url_failed", url=url, browser=browser, error=str(e))
        return f"Failed to open '{url}' in {browser}: {str(e)}"
```

**Note:** Full implementation code for all 15 browser tools will be provided in a separate Phase 11.2 implementation guide. The pattern above shows the correct approach using `@agent.tool` decorator with optional `browser` parameter (defaults to "Safari").

**Browser Compatibility:**
- ✅ **Safari**: Full support (best option)
- ⚠️ **Chrome**: Requires "Allow JavaScript from Apple Events" in View → Developer menu
- ⚠️ **Firefox**: Limited AppleScript support

---

## Phase 11.3-11.10: Remaining Tool Categories

### Quick Summary

Each phase follows the same pattern as 11.1 and 11.2:

**Phase 11.3: Window Tools (10 commands)** - 4h
- window_resize, window_move, window_minimize, window_maximize
- window_fullscreen, window_tile_left, window_tile_right
- window_center, window_get_bounds, window_close
- **Dependencies:** PyObjC (already installed in 11.1)

**Phase 11.4: System Tools (10 commands - SAFE ONLY)** - 4h
- system_read_file, system_write_file, system_copy_file, system_move_file
- system_list_files, system_create_directory, system_get_file_info
- system_file_exists, system_get_disk_space, system_download_file
- **Dependencies:** Built-in Python libraries (os, shutil, pathlib, requests)
- ⚠️ **REMOVED:** `system_delete_file`, `system_delete_directory` (moved to Phase 11.11)

**Phase 11.5: Keyboard Tools (5 commands)** - 3h
- keyboard_type_text, keyboard_press_key, keyboard_hotkey
- keyboard_press_and_hold, keyboard_release
- **Dependencies:** `pyobjc-framework-Quartz==12.0` (native CGEvent APIs)
- **Native API:** Uses `Quartz.CoreGraphics.CGEvent` for keyboard control

**Phase 11.6: Mouse Tools (8 commands)** - 4h
- mouse_move, mouse_click, mouse_double_click
- mouse_right_click, mouse_drag, mouse_scroll
- mouse_get_position, mouse_click_at
- **Dependencies:** `pyobjc-framework-Quartz==12.0` (already installed in 11.5)
- **Native API:** Uses `Quartz.CoreGraphics.CGEvent` for mouse control

**Phase 11.7: Clipboard Tools (4 commands)** - 2h
- clipboard_get_text, clipboard_set_text
- clipboard_get_image, clipboard_set_image
- **Dependencies:** `Pillow==12.0.0` (for image handling)
- **Native API:** Uses `AppKit.NSPasteboard` (in Cocoa, already installed)
- **Note:** pyperclip is installed but NOT used - NSPasteboard handles text + images

**Phase 11.8: Display Tools (5 commands)** - 3h
- display_take_screenshot, display_get_brightness
- display_set_brightness, display_list_displays
- display_get_resolution
- **Dependencies:** `pyobjc-framework-Quartz==12.0` (for display APIs), `Pillow==12.0.0` (for screenshots)
- **Native API:** Uses `Quartz.CoreGraphics` for screenshots and display management

**Phase 11.9: Media Tools (15 commands)** - 5h
- media_play, media_pause, media_next_track, media_previous_track
- media_get_current_track, media_set_volume, media_get_volume
- media_mute, media_unmute, media_shuffle_on, media_shuffle_off
- media_repeat_on, media_repeat_off, media_seek, media_get_playback_state
- **Dependencies:** AppleScript via `appscript` (already installed)

**Phase 11.10: Finder Tools (6 commands - SAFE ONLY)** - 3h
- finder_open_folder, finder_reveal_in_finder
- finder_new_folder, finder_select_file
- finder_get_selection, finder_get_info
- **Dependencies:** AppleScript via `appscript` (already installed)
- ⚠️ **REMOVED:** `finder_trash_file`, `finder_empty_trash` (moved to Phase 11.11)

### Phase 11.11: Dangerous Operations (FUTURE)

**⚠️ NOT IMPLEMENTED IN CURRENT PHASE 11**

This phase will be implemented AFTER Phase 11.10 is complete and stable.

**Goal:** Add confirmation mechanisms for destructive operations

**Tools to Add (with safety):**
- system_delete_file (requires confirmation)
- system_delete_directory (requires confirmation)
- finder_trash_file (requires confirmation)
- finder_empty_trash (requires confirmation + double confirmation)

**Safety Mechanisms:**
1. User confirmation prompt before execution
2. Dry-run mode to preview changes
3. Trash/recycle bin instead of permanent delete
4. Whitelist/blacklist for protected paths
5. Undo functionality where possible

**Time:** 4 hours (including safety testing)

---

## Testing & Validation

### Final System Prompt

After Phase 11.10, update `SYSTEM_PROMPT` with complete tool list:

```python
SYSTEM_PROMPT = """You are an intelligent macOS automation assistant powered by Baby AI.

**IMPORTANT: Always respond in the same language as the user.**

## Available Tools (84 total)

### Application Control (10)
- open_app, close_app, list_running_apps, is_app_running
- focus_app, hide_app, unhide_app, restart_app
- get_app_info, launch_app_with_file

### Browser Automation (15)
- browser_open_url, browser_close_tab, browser_new_tab
- browser_go_back, browser_go_forward, browser_reload
- browser_get_current_url, browser_get_page_title
- browser_scroll_up, browser_scroll_down
- browser_scroll_to_top, browser_scroll_to_bottom
- browser_find_text, browser_click_link, browser_switch_tab

### Window Management (10)
- window_resize, window_move, window_minimize, window_maximize
- window_fullscreen, window_tile_left, window_tile_right
- window_center, window_get_bounds, window_close

### System & File Operations (10 - SAFE ONLY)
- system_read_file, system_write_file, system_copy_file, system_move_file
- system_list_files, system_create_directory, system_get_file_info
- system_file_exists, system_get_disk_space, system_download_file

### Keyboard Control (5)
- keyboard_type_text, keyboard_press_key, keyboard_hotkey
- keyboard_press_and_hold, keyboard_release

### Mouse Control (8)
- mouse_move, mouse_click, mouse_double_click, mouse_right_click
- mouse_drag, mouse_scroll, mouse_get_position, mouse_click_at

### Clipboard Operations (4)
- clipboard_get_text, clipboard_set_text
- clipboard_get_image, clipboard_set_image

### Display Management (5)
- display_take_screenshot, display_get_brightness, display_set_brightness
- display_list_displays, display_get_resolution

### Media Control (15)
- media_play, media_pause, media_next_track, media_previous_track
- media_get_current_track, media_set_volume, media_get_volume
- media_mute, media_unmute, media_shuffle_on, media_shuffle_off
- media_repeat_on, media_repeat_off, media_seek, media_get_playback_state

### Finder Operations (6 - SAFE ONLY)
- finder_open_folder, finder_reveal_in_finder, finder_new_folder
- finder_select_file, finder_get_selection, finder_get_info

Remember: Be helpful, friendly, and conversational!
"""
```

### End-to-End Testing

**Complex multi-tool workflows:**

```bash
# Workflow 1: Research and save
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Apri Google, cerca tutorial Python, e salva l URL in tutorials.txt", "stream": false}'

# Workflow 2: Window management
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Apri Safari e TextEdit, affianca Safari a sinistra e TextEdit a destra", "stream": false}'

# Workflow 3: Screenshot and organize
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Fai uno screenshot, salvalo sulla Scrivania, crea una cartella Screenshots, e spostalo li", "stream": false}'

# Verify tool calling in logs
tail -f /tmp/baby-ai-backend.log | grep -E "tool:|running tool:"
```

### Success Criteria

Phase 11 is complete when:

- ✅ All 84 tools implemented in `pydantic_agent.py`
- ✅ All tools use `@agent.tool` decorator
- ✅ All tools tested individually
- ✅ System prompt documents all capabilities
- ✅ Complex workflows tested successfully
- ✅ No regressions from Phase 10.1
- ✅ All dependencies installed and verified
- ✅ Code committed and tagged

### Final Commit

```bash
git add .
git commit -m "feat: Phase 11 complete (11.1-11.10) - 84 safe tools

Implemented full multi-tool system with Pydantic AI:
- 10 AppAgent tools
- 15 Browser tools
- 10 Window tools
- 10 System tools (SAFE ONLY - no delete operations)
- 5 Keyboard tools
- 8 Mouse tools
- 4 Clipboard tools
- 5 Display tools
- 15 Media tools
- 6 Finder tools (SAFE ONLY - no trash operations)

Total: 84 tools, all registered with @agent.tool decorator
Architecture: Single unified Pydantic AI agent
Testing: ✅ All tools tested, complex workflows validated
Safety: ⚠️ Dangerous operations moved to Phase 11.11

Dependencies installed (NATIVE macOS approach):
- pyobjc-framework-Quartz==12.0  (NEW - for display, keyboard, mouse)
- Pillow==12.0.0                 (NEW - for images)
- pyobjc-framework-Cocoa==12.0   (already installed)
- appscript==1.4.0               (already installed)

Native APIs used:
- NSWorkspace, NSPasteboard (AppKit/Cocoa)
- CGEvent, CGDisplay (Quartz/CoreGraphics)
- AppleScript (via appscript)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push
git tag v0.2.0-phase11-pydantic-ai
git push --tags
```

---

## Key Differences from v2.1

### What's Gone

- ❌ No `BaseAgent` class
- ❌ No `AppAgent.get_tool_functions()`
- ❌ No separate agent files per category
- ❌ No `src/orchestrator/orchestrator.py` modification
- ❌ No manual tool collection or merging
- ❌ No dangerous delete/trash operations (moved to Phase 11.11)

### What's New

- ✅ All tools in single file: `src/agents/pydantic_agent.py`
- ✅ All tools use `@agent.tool` decorator
- ✅ Pydantic AI handles tool calling automatically
- ✅ Simpler architecture, less code
- ✅ All imports at top of file (consistent pattern)
- ✅ **Native macOS APIs only** - professional approach
- ✅ Only 2 new dependencies (Quartz + Pillow)
- ✅ Safety-first approach (dangerous ops in separate phase)

### Migration Notes

**If you have v2.1 or v3.0 code:**
1. Delete old agent files (app_agent.py, browser_agent.py, etc.)
2. Add all tools to `pydantic_agent.py` with `@agent.tool`
3. Remove orchestrator modifications
4. Install all dependencies from "Complete Dependencies" section
5. Test with Pydantic AI runner

---

## Troubleshooting

### Accessibility Permissions

**Error:** "Accessibility permissions denied"

**Fix:** System Settings → Privacy & Security → Accessibility → Add Python or Terminal

### PyObjC Import Errors

**Error:** "No module named 'AppKit'"

**Fix:**
```bash
pip install pyobjc-framework-Cocoa==12.0
# If still failing, install full PyObjC suite:
pip install pyobjc==12.0
```

### Browser Commands Not Working

- **Safari:** Works best (full support)
- **Chrome:** Requires "Allow JavaScript from Apple Events" in View → Developer
- **Firefox:** Limited AppleScript support

### Tool Not Being Called

**Issue:** LLM doesn't call your tool

**Fix:**
1. Check docstring is descriptive
2. Verify `@agent.tool` decorator is present
3. Check function signature has `ctx: RunContext` first
4. Restart backend to reload tools
5. Check logs for tool registration: `tail -f /tmp/baby-ai-backend.log | grep "tool:"`

### Import Errors After Phase 11.1

**Error:** "No module named 'time'" or "No module named 'subprocess'"

**Fix:** These are built-in Python modules. Check that imports are at the TOP of `pydantic_agent.py`, not inside functions.

### CGEvent Permission Issues (Native Keyboard/Mouse)

**Error:** "CGEvent permission denied" or keyboard/mouse tools not working

**Fix:** System Settings → Privacy & Security → Accessibility → Add Python interpreter or Terminal

**Note:** Native CGEvent APIs require Accessibility permissions (same as pyautogui, but more reliable)

---

**End of Phase 11 Pydantic AI Implementation Plan v3.2**

**Changes from v3.1 (NATIVE macOS APIs):**
- ✅ Removed pyautogui dependency - using native CGEvent instead
- ✅ Removed pynput dependency - redundant with CGEvent
- ✅ Removed pyperclip usage - using native NSPasteboard instead
- ✅ Kept Pillow for image handling
- ✅ Only 2 new dependencies: Quartz + Pillow (instead of 4)
- ✅ Updated Phase 11.5 (Keyboard) to use CGEvent APIs
- ✅ Updated Phase 11.6 (Mouse) to use CGEvent APIs
- ✅ Updated Phase 11.7 (Clipboard) to use NSPasteboard + Pillow
- ✅ Updated Phase 11.8 (Display) to use Quartz CoreGraphics
- ✅ Professional macOS-native approach throughout

**Why Native APIs?**
- Better permissions handling and macOS integration
- Better performance (no cross-platform overhead)
- More features (NSPasteboard: text + images vs pyperclip: text only)
- Professional code using Apple frameworks
- Fewer dependencies (2 vs 4)

**Status:** ✅ Ready for Implementation
**Next Step:** Implement Phase 11.1 following Step 11.1.1 - 11.1.6
