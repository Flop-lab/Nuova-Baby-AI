# Phase 11: Complete Multi-Agent System - Design Document

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
12. [Architecture Updates](#architecture-updates)
13. [Testing Strategy](#testing-strategy)
14. [Security & Safety](#security--safety)

---

## Overview

### Purpose

Phase 11 completes the multi-agent system by implementing all 10 specialized agents with their full command sets from the original Baby AI. Each sub-phase adds one agent, tests it thoroughly, then proceeds to the next.

### Approach

For each agent:
1. **Analyze** commands from old Baby AI's corresponding service
2. **Map** TypeScript/AppleScript commands to Python + appscript
3. **Implement** agent with all tools
4. **Test** with unit tests, integration tests, and manual curl tests
5. **Validate** before moving to next agent

### Command Count Summary

| Phase | Agent | Commands | Source |
|-------|-------|----------|--------|
| 11.1 | AppAgent | 10 | appService.ts |
| 11.2 | BrowserAgent | 15 | browserService.ts |
| 11.3 | WindowAgent | 10 | windowService.ts |
| 11.4 | SystemAgent | 12 | systemService.ts |
| 11.5 | KeyboardAgent | 5 | keyboardService.ts |
| 11.6 | MouseAgent | 8 | mouseService.ts |
| 11.7 | ClipboardAgent | 4 | clipboardService.ts |
| 11.8 | DisplayAgent | 5 | displayService.ts |
| 11.9 | MediaAgent | 15 | mediaService.ts |
| 11.10 | FinderAgent | 8 | finderService.ts |
| **Total** | **10 agents** | **92 commands** | |

---

## Phase 11.1: Complete AppAgent

### Current State (from Phase 1-10)

**Existing commands:**
- `open_app(app_name: str)` - Opens/activates an app
- `close_app(app_name: str)` - Closes an app

### New Commands to Add

Based on `appService.ts` from old Baby AI:

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `activate` | `activate_app` | app_name: str | Activates an app (alias of open_app) |
| `quit` | `quit_app` | app_name: str | Quits an app gracefully |
| `listRunning` | `list_running_apps` | none | Lists all running apps |
| `launch` | `launch_app` | app_name: str | Launches app without activating |
| `forceQuit` | `force_quit_app` | app_name: str | Force quits an app (dangerous) |
| `hide` | `hide_app` | app_name: str | Hides an app |
| `show` | `show_app` | app_name: str | Shows a hidden app |
| `isRunning` | `is_app_running` | app_name: str | Checks if app is running |
| `getFrontmost` | `get_frontmost_app` | none | Gets the frontmost app |
| `switchTo` | `switch_to_app` | app_name: str | Switches to an app (alias of activate) |

### Tool Consolidation

**Aliases to handle:**
- `activate_app` and `switch_to_app` → both map to same implementation (activate)
- `open_app` (existing) → also activates, so same as activate
- `quit_app` and `close_app` (existing) → similar but quit is more graceful

**Recommendation:**
- Keep `open_app` and `close_app` as primary tools (already in Phase 1-10)
- Add all other commands as distinct tools
- Document that `open_app` = `activate_app` = `switch_to_app` in system prompt

### Complete AppAgent Tool List

```python
class AppAgent:
    """Agent for macOS application control"""
    
    domain = "app"
    
    @staticmethod
    def get_tools() -> list[Tool]:
        return [
            # Phase 1-10 (existing)
            Tool(
                name="open_app",
                description="Opens and activates a macOS application",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            Tool(
                name="close_app",
                description="Closes a macOS application",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            
            # Phase 11.1 (new)
            Tool(
                name="launch_app",
                description="Launches an application without activating it",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            Tool(
                name="quit_app",
                description="Gracefully quits an application",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            Tool(
                name="force_quit_app",
                description="Force quits an application (use only when app is unresponsive)",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                },
                dangerous=True  # Requires confirmation
            ),
            Tool(
                name="hide_app",
                description="Hides an application",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            Tool(
                name="show_app",
                description="Shows a hidden application",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                }
            ),
            Tool(
                name="is_app_running",
                description="Checks if an application is currently running",
                parameters={
                    "app_name": {"type": "string", "description": "Name of the application"}
                },
                returns="bool"
            ),
            Tool(
                name="list_running_apps",
                description="Lists all currently running applications",
                parameters={},
                returns="list[str]"
            ),
            Tool(
                name="get_frontmost_app",
                description="Gets the name of the frontmost (active) application",
                parameters={},
                returns="str"
            ),
        ]
```

### Implementation Notes

**AppleScript mappings:**

```python
# launch_app
app(app_name).launch()

# quit_app
app(app_name).quit()

# force_quit_app (requires subprocess for killall)
subprocess.run(['killall', app_name])

# hide_app
app('System Events').processes[app_name].visible.set(False)

# show_app
app('System Events').processes[app_name].visible.set(True)

# is_app_running
app_name in [p.name() for p in app('System Events').processes()]

# list_running_apps
[p.name() for p in app('System Events').processes() if not p.background_only()]

# get_frontmost_app
[p.name() for p in app('System Events').processes() if p.frontmost()][0]
```

### Safety Considerations

**Dangerous commands:**
- `force_quit_app` - Can cause data loss, requires confirmation

**Accessibility permissions required:**
- `hide_app`, `show_app`, `is_app_running`, `list_running_apps`, `get_frontmost_app` all require System Events access

---

## Phase 11.2: BrowserAgent

### Purpose

Controls web browsers (Safari, Chrome, Firefox) for navigation, tab management, and page interaction.

### Commands from browserService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `open` | `browser_open_url` | url: str, browser: str | Opens URL in browser |
| `closeTab` | `browser_close_tab` | browser: str | Closes current tab |
| `newTab` | `browser_new_tab` | url: str, browser: str | Opens new tab with URL |
| `goBack` | `browser_go_back` | browser: str | Navigates back |
| `goForward` | `browser_go_forward` | browser: str | Navigates forward |
| `reload` | `browser_reload` | browser: str | Reloads current page |
| `getCurrentUrl` | `browser_get_current_url` | browser: str | Gets current URL |
| `getPageContent` | `browser_get_page_content` | browser: str | Gets page text content |
| `scrollUp` | `browser_scroll_up` | browser: str, amount?: int | Scrolls up |
| `scrollDown` | `browser_scroll_down` | browser: str, amount?: int | Scrolls down |
| `scrollToTop` | `browser_scroll_to_top` | browser: str | Scrolls to top |
| `scrollToBottom` | `browser_scroll_to_bottom` | browser: str | Scrolls to bottom |
| `findText` | `browser_find_text` | text: str, browser: str | Finds text on page |
| `clickLink` | `browser_click_link` | text: str, browser: str | Clicks link by text |
| `switchTab` | `browser_switch_tab` | index: int, browser: str | Switches to tab by index |

### Tool Schema Example

```python
Tool(
    name="browser_open_url",
    description="Opens a URL in the specified browser",
    parameters={
        "url": {"type": "string", "description": "URL to open"},
        "browser": {"type": "string", "description": "Browser name (Safari, Chrome, Firefox)", "default": "Safari"}
    }
)
```

### Implementation Notes

**AppleScript mappings:**

```python
# browser_open_url
app(browser).open_location(url)

# browser_close_tab
app(browser).windows[0].current_tab.close()

# browser_new_tab
app(browser).windows[0].make(new=k.tab, with_properties={k.URL: url})

# browser_go_back
app(browser).windows[0].go_back()

# browser_reload (via JavaScript)
app(browser).do_javascript("location.reload()", in_=app(browser).front_document)

# browser_get_current_url
app(browser).front_document.URL()

# browser_scroll_down (via JavaScript)
app(browser).do_javascript(f"window.scrollBy(0, {amount})", in_=app(browser).front_document)
```

### Browser Compatibility

| Command | Safari | Chrome | Firefox |
|---------|--------|--------|---------|
| open_url | ✅ | ✅ | ✅ |
| close_tab | ✅ | ✅ | ⚠️ Limited |
| new_tab | ✅ | ✅ | ⚠️ Limited |
| navigation | ✅ | ✅ | ⚠️ Limited |
| JavaScript | ✅ | ✅ | ❌ No |

**Note:** Safari has best AppleScript support. Chrome is good. Firefox is limited.

---

## Phase 11.3: WindowAgent

### Purpose

Manages window positioning, sizing, and states for any macOS application.

### Commands from windowService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `resize` | `window_resize` | app_name: str, width: int, height: int | Resizes window |
| `move` | `window_move` | app_name: str, x: int, y: int | Moves window |
| `minimize` | `window_minimize` | app_name: str | Minimizes window |
| `maximize` | `window_maximize` | app_name: str | Maximizes window |
| `fullscreen` | `window_fullscreen` | app_name: str | Sets window to fullscreen |
| `tileLeft` | `window_tile_left` | app_name: str | Tiles window to left half |
| `tileRight` | `window_tile_right` | app_name: str | Tiles window to right half |
| `center` | `window_center` | app_name: str | Centers window |
| `getBounds` | `window_get_bounds` | app_name: str | Gets window bounds |
| `close` | `window_close` | app_name: str | Closes front window |

### Implementation Notes

**AppleScript mappings:**

```python
# window_resize
app(app_name).windows[0].bounds.set([0, 0, width, height])

# window_move
app(app_name).windows[0].position.set([x, y])

# window_minimize
app(app_name).windows[0].miniaturized.set(True)

# window_fullscreen (via System Events)
app('System Events').processes[app_name].windows[0].attributes['AXFullScreen'].value.set(True)

# window_tile_left (hardcoded for 1920x1080)
app(app_name).windows[0].bounds.set([0, 0, 960, 1080])

# window_get_bounds
app(app_name).windows[0].bounds()
```

### Dynamic Screen Resolution

**Issue:** Old Baby AI hardcodes 1920x1080 for maximize/tile operations.

**Solution for Phase 11.3:**
```python
import AppKit

def get_screen_size():
    screen = AppKit.NSScreen.mainScreen()
    frame = screen.frame()
    return int(frame.size.width), int(frame.size.height)

# Use in window_maximize
width, height = get_screen_size()
app(app_name).windows[0].bounds.set([0, 0, width, height])
```

---

## Phase 11.4: SystemAgent

### Purpose

Handles file system operations, shell commands, and system-level tasks.

### Commands from systemService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `readFile` | `system_read_file` | path: str | Reads file content |
| `writeFile` | `system_write_file` | path: str, content: str | Writes file content |
| `deleteFile` | `system_delete_file` | path: str | Deletes a file |
| `copyFile` | `system_copy_file` | source: str, destination: str | Copies a file |
| `moveFile` | `system_move_file` | source: str, destination: str | Moves a file |
| `download` | `system_download` | url: str, destination: str | Downloads file from URL |
| `listFiles` | `system_list_files` | path: str | Lists files in directory |
| `createDirectory` | `system_create_directory` | path: str | Creates a directory |
| `deleteDirectory` | `system_delete_directory` | path: str | Deletes a directory |
| `getFileInfo` | `system_get_file_info` | path: str | Gets file metadata |
| `fileExists` | `system_file_exists` | path: str | Checks if file exists |
| `getDiskSpace` | `system_get_disk_space` | none | Gets disk space info |

### Implementation Notes

**Python standard library (preferred over shell):**

```python
import os
import shutil
import subprocess
from pathlib import Path

# system_read_file
Path(path).read_text()

# system_write_file
Path(path).write_text(content)

# system_delete_file
Path(path).unlink()

# system_copy_file
shutil.copy2(source, destination)

# system_move_file
shutil.move(source, destination)

# system_download
subprocess.run(['curl', '-L', '-o', destination, url])

# system_list_files
os.listdir(path)

# system_create_directory
Path(path).mkdir(parents=True, exist_ok=True)

# system_file_exists
Path(path).exists()

# system_get_disk_space
shutil.disk_usage(path)
```

### Safety Considerations

**Dangerous commands (require confirmation):**
- `system_delete_file`
- `system_delete_directory`
- `system_write_file` (if overwriting existing file)

**Path validation:**
- Sanitize all paths to prevent directory traversal
- Warn on operations outside user home directory
- Block operations on system directories (/System, /Library, /usr, /bin, /sbin)

---

## Phase 11.5: KeyboardAgent

### Purpose

Simulates keyboard input for typing, hotkeys, and special keys.

### Commands from keyboardService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `keystroke` | `keyboard_keystroke` | chars: str | Types characters |
| `hotkey` | `keyboard_hotkey` | key: str, modifiers: str | Presses hotkey combination |
| `pressKey` | `keyboard_press_key` | key: str | Presses special key |
| `typeText` | `keyboard_type_text` | text: str | Types text (alias of keystroke) |
| `paste` | `keyboard_paste` | none | Simulates Cmd+V |

### Implementation Notes

**AppleScript mappings:**

```python
# keyboard_keystroke
app('System Events').keystroke(chars)

# keyboard_hotkey
app('System Events').keystroke(key, using=[k.command_down, k.shift_down])

# keyboard_press_key (using key codes)
app('System Events').key_code(36)  # Return key

# keyboard_paste
app('System Events').keystroke('v', using=k.command_down)
```

### Key Code Mapping

```python
KEY_CODES = {
    'return': 36,
    'enter': 36,
    'tab': 48,
    'space': 49,
    'delete': 51,
    'escape': 53,
    'esc': 53,
    'up': 126,
    'down': 125,
    'left': 123,
    'right': 124,
}
```

### Modifier Keys

```python
MODIFIERS = {
    'command': k.command_down,
    'cmd': k.command_down,
    'shift': k.shift_down,
    'option': k.option_down,
    'alt': k.option_down,
    'control': k.control_down,
    'ctrl': k.control_down,
}
```

---

## Phase 11.6: MouseAgent

### Purpose

Controls mouse movement, clicks, and drag operations.

### Commands from mouseService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `click` | `mouse_click` | none | Clicks at current position |
| `doubleClick` | `mouse_double_click` | none | Double clicks at current position |
| `rightClick` | `mouse_right_click` | none | Right clicks at current position |
| `move` | `mouse_move` | x: int, y: int | Moves mouse to position |
| `drag` | `mouse_drag` | from_x: int, from_y: int, to_x: int, to_y: int | Drags from one position to another |
| `scroll` | `mouse_scroll` | direction: str, amount: int | Scrolls up or down |
| `getPosition` | `mouse_get_position` | none | Gets current mouse position |
| `clickAt` | `mouse_click_at` | x: int, y: int | Clicks at specific position |

### Implementation Notes

**AppleScript mappings:**

```python
# mouse_move
app('System Events').mouse.position.set([x, y])

# mouse_click_at
app('System Events').click_at([x, y])

# mouse_drag
app('System Events').mouse.position.set([from_x, from_y])
time.sleep(0.1)
# Mouse down/up requires System Events scripting
```

**Note:** Mouse control via appscript is limited. May need to use PyObjC's Quartz for more reliable mouse events.

---

## Phase 11.7: ClipboardAgent

### Purpose

Manages system clipboard for copy/paste operations.

### Commands from clipboardService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `get` | `clipboard_get` | none | Gets clipboard content |
| `set` | `clipboard_set` | text: str | Sets clipboard content |
| `clear` | `clipboard_clear` | none | Clears clipboard |
| `getHistory` | `clipboard_get_history` | none | Gets clipboard history (not available) |

### Implementation Notes

**Using subprocess (pbcopy/pbpaste):**

```python
import subprocess

# clipboard_get
subprocess.run(['pbpaste'], capture_output=True, text=True).stdout

# clipboard_set
subprocess.run(['pbcopy'], input=text, text=True)

# clipboard_clear
subprocess.run(['pbcopy'], input='', text=True)
```

**Note:** `clipboard_get_history` is not available on macOS without third-party tools. Return error message explaining this.

---

## Phase 11.8: DisplayAgent

### Purpose

Handles screen capture and display settings.

### Commands from displayService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `screenshot` | `display_screenshot` | path: str | Takes full screen screenshot |
| `screenshotWindow` | `display_screenshot_window` | path: str | Takes window screenshot (interactive) |
| `screenshotSelection` | `display_screenshot_selection` | path: str | Takes selection screenshot (interactive) |
| `getBrightness` | `display_get_brightness` | none | Gets display brightness |
| `setBrightness` | `display_set_brightness` | level: float | Sets display brightness (0.0-1.0) |

### Implementation Notes

**Using subprocess (screencapture):**

```python
import subprocess

# display_screenshot
subprocess.run(['screencapture', path])

# display_screenshot_window (interactive - user clicks window)
subprocess.run(['screencapture', '-w', path])

# display_screenshot_selection (interactive - user selects area)
subprocess.run(['screencapture', '-s', path])
```

**Brightness control (via AppleScript):**

```python
# display_get_brightness
app('System Events').displays[0].brightness()

# display_set_brightness
app('System Events').displays[0].brightness.set(level)
```

---

## Phase 11.9: MediaAgent

### Purpose

Controls media playback (Music app) and handles image/video processing.

### Commands from mediaService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `play` | `media_play` | none | Plays music |
| `pause` | `media_pause` | none | Pauses music |
| `stop` | `media_stop` | none | Stops music |
| `nextTrack` | `media_next_track` | none | Next track |
| `previousTrack` | `media_previous_track` | none | Previous track |
| `volumeUp` | `media_volume_up` | amount?: int | Increases volume |
| `volumeDown` | `media_volume_down` | amount?: int | Decreases volume |
| `setVolume` | `media_set_volume` | level: int | Sets volume (0-100) |
| `getVolume` | `media_get_volume` | none | Gets current volume |
| `mute` | `media_mute` | none | Mutes audio |
| `imageConvert` | `media_image_convert` | input: str, output: str | Converts image format |
| `imageResize` | `media_image_resize` | input: str, output: str, width: int, height: int | Resizes image |
| `imageGrayscale` | `media_image_grayscale` | input: str, output: str | Converts to grayscale |
| `videoConvert` | `media_video_convert` | input: str, output: str | Converts video format |
| `extractAudio` | `media_extract_audio` | input_video: str, output_audio: str | Extracts audio from video |

### Implementation Notes

**Music control (via AppleScript):**

```python
# media_play
app('Music').play()

# media_pause
app('Music').pause()

# media_next_track
app('Music').next_track()

# media_set_volume (system volume, not Music app)
subprocess.run(['osascript', '-e', f'set volume output volume {level}'])
```

**Image/Video processing:**

**Note:** Requires external tools (ImageMagick, ffmpeg). These are NOT bundled with Baby AI.

**Recommendation:** 
- Check if tools are installed before executing
- Return helpful error if not installed: "ImageMagick not found. Install with: brew install imagemagick"
- Mark these commands as "requires external dependencies" in documentation

---

## Phase 11.10: FinderAgent

### Purpose

Controls Finder for file browsing and management.

### Commands from finderService.ts

| Old Command | New Tool Name | Parameters | Description |
|-------------|---------------|------------|-------------|
| `openFolder` | `finder_open_folder` | path: str | Opens folder in Finder |
| `selectFile` | `finder_select_file` | path: str | Selects file in Finder |
| `getSelection` | `finder_get_selection` | none | Gets selected files |
| `copyFiles` | `finder_copy_files` | source: str, destination: str | Copies files |
| `moveFiles` | `finder_move_files` | source: str, destination: str | Moves files |
| `deleteFiles` | `finder_delete_files` | path: str | Moves to trash |
| `search` | `finder_search` | query: str, location?: str | Searches files (Spotlight) |
| `newFolder` | `finder_new_folder` | path: str, name: str | Creates new folder |

### Implementation Notes

**AppleScript mappings:**

```python
# finder_open_folder
app('Finder').open(mactypes.Alias(path))

# finder_select_file
app('Finder').select(mactypes.Alias(path))

# finder_get_selection
app('Finder').selection()

# finder_delete_files (moves to trash, not permanent delete)
app('Finder').delete(mactypes.Alias(path))

# finder_search (using Spotlight via mdfind)
subprocess.run(['mdfind', '-onlyin', location, query], capture_output=True, text=True).stdout
```

### Safety Considerations

**Note:** `finder_delete_files` moves to trash (recoverable), not permanent deletion. This is safer than `system_delete_file`.

---

## Architecture Updates

### Agent Registry

Update `src/orchestrator/orchestrator.py` to register all agents:

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
```

### Tool Registration

All tools from all agents are collected and passed to LLM:

```python
def get_all_tools() -> list[Tool]:
    tools = []
    for agent_class in AGENTS:
        tools.extend(agent_class.get_tools())
    return tools
```

### System Prompt Updates

Update system prompt to include:
- All 92 commands with descriptions
- Safety warnings for dangerous commands
- Examples of multi-agent workflows
- Guidance on when to use which agent

---

## Testing Strategy

### Per-Agent Testing (Each Phase 11.x)

**1. Unit Tests**
- Mock appscript calls
- Test parameter validation
- Test error handling
- Test edge cases

**2. Integration Tests (macOS only)**
- Real appscript calls
- Test with actual apps
- Verify expected behavior
- Clean up after tests

**3. Manual Tests (curl)**
- Test via `/api/chat` endpoint
- Verify LLM can invoke tools correctly
- Test error recovery
- Test multi-step workflows

### Test Organization

```
tests/
├── unit/
│   ├── test_app_agent.py
│   ├── test_browser_agent.py
│   ├── test_window_agent.py
│   ├── test_system_agent.py
│   ├── test_keyboard_agent.py
│   ├── test_mouse_agent.py
│   ├── test_clipboard_agent.py
│   ├── test_display_agent.py
│   ├── test_media_agent.py
│   └── test_finder_agent.py
├── integration/
│   ├── test_app_agent_integration.py
│   ├── test_browser_agent_integration.py
│   └── ... (one per agent)
└── manual/
    └── test_commands.md  # curl commands for manual testing
```

### Test Execution

```bash
# Unit tests (run on any platform)
pytest tests/unit/

# Integration tests (macOS only)
pytest tests/integration/ -m "darwin"

# Specific agent tests
pytest tests/unit/test_app_agent.py -v
```

---

## Security & Safety

### Dangerous Commands

Commands that require user confirmation:

| Command | Risk | Mitigation |
|---------|------|------------|
| `force_quit_app` | Data loss | Require confirmation |
| `system_delete_file` | Data loss | Require confirmation, block system paths |
| `system_delete_directory` | Data loss | Require confirmation, block system paths |
| `system_write_file` | Overwrite data | Warn if file exists |
| `media_image_convert` | Command injection | Sanitize paths |
| `media_video_convert` | Command injection | Sanitize paths |

### Confirmation Mechanism

```python
class ToolResult:
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    requires_confirmation: bool = False
    confirmation_message: Optional[str] = None
```

When `requires_confirmation=True`, the orchestrator:
1. Returns confirmation message to user
2. Waits for user approval
3. Re-executes with confirmation flag set

### Path Sanitization

```python
BLOCKED_PATHS = [
    '/System',
    '/Library',
    '/usr',
    '/bin',
    '/sbin',
    '/private',
]

def is_safe_path(path: str) -> bool:
    abs_path = os.path.abspath(path)
    for blocked in BLOCKED_PATHS:
        if abs_path.startswith(blocked):
            return False
    return True
```

### Accessibility Permissions

Many commands require macOS Accessibility permissions:
- All KeyboardAgent commands
- All MouseAgent commands
- Some AppAgent commands (hide, show, list_running)
- Some WindowAgent commands (fullscreen)

**User must grant permissions:**
System Preferences → Security & Privacy → Privacy → Accessibility → Add Baby AI

---

## Dependencies

### Python Packages (add to requirements.txt)

```
# Already in Phase 1-10
appscript==1.4.0

# New for Phase 11
pyobjc-framework-Cocoa==10.3.1  # For screen resolution, mouse control
pyobjc-framework-Quartz==10.3.1  # For advanced mouse events
```

### External Tools (optional, not bundled)

- **ImageMagick** - for image processing (media_image_*)
- **ffmpeg** - for video processing (media_video_*, media_extract_audio)

**Note:** These are NOT required for core functionality. Commands will fail gracefully with helpful error messages if tools are missing.

---

## Out of Scope for Phase 11

**Not implementing:**
- Multi-agent coordination (Phase 12+)
- Agent-to-agent communication
- Parallel tool execution
- Advanced error recovery strategies
- Plugin system for custom agents
- Voice control
- Vision/OCR capabilities

**These are for future phases.**

---

## Success Criteria

Phase 11 is complete when:

✅ All 10 agents implemented (11.1-11.10)  
✅ All 92 commands functional  
✅ Unit tests pass for all agents  
✅ Integration tests pass on macOS  
✅ Manual curl tests successful  
✅ Documentation complete  
✅ Safety mechanisms in place  
✅ No regressions from Phase 1-10  

---

## Estimated Timeline

| Phase | Agent | Commands | Estimated Time |
|-------|-------|----------|----------------|
| 11.1 | AppAgent | 10 | 4 hours |
| 11.2 | BrowserAgent | 15 | 6 hours |
| 11.3 | WindowAgent | 10 | 4 hours |
| 11.4 | SystemAgent | 12 | 5 hours |
| 11.5 | KeyboardAgent | 5 | 3 hours |
| 11.6 | MouseAgent | 8 | 4 hours |
| 11.7 | ClipboardAgent | 4 | 2 hours |
| 11.8 | DisplayAgent | 5 | 3 hours |
| 11.9 | MediaAgent | 15 | 5 hours |
| 11.10 | FinderAgent | 8 | 4 hours |
| **Total** | **10 agents** | **92 commands** | **40 hours (~1 week)** |

---

## Next Steps

After Phase 11 completion:
1. **Phase 12:** Multi-agent coordination and workflows
2. **Phase 13:** Advanced error recovery and retry strategies
3. **Phase 14:** Performance optimization and caching
4. **Phase 15:** Plugin system for custom agents
5. **Phase 16:** Voice control integration
6. **Phase 17:** Vision/OCR capabilities

---

**End of Phase 11 Design Document**
