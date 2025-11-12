# Baby AI - Phase 1.1 Design Document
## App Agent POC - Python Rewrite

**Version:** 1.1  
**Date:** November 12, 2025  
**Author:** Devin AI  
**Status:** Draft for Review

---

## 1. Versions

### 1.1 Ollama Versions (IMPORTANT: Two Different Components)

**Ollama Server** (macOS binary to bundle with Tauri):
- **Version:** v0.12.10
- **Source:** https://github.com/ollama/ollama/releases
- **Purpose:** Local LLM inference server (bundled in Phase 1.1)
- **Installation:** Bundled with PyInstaller in Tauri app

**ollama-python SDK** (Python client library):
- **Version:** v0.6.0
- **Source:** https://github.com/ollama/ollama-python/releases
- **Purpose:** Python API client to communicate with Ollama server
- **Installation:** `pip install ollama==0.6.0` (in requirements.txt)

**Note:** These two components have **independent versioning**. The server is at v0.12.10 while the Python SDK is at v0.6.0. Both are the latest stable versions as of November 2025.

### 1.2 All Component Versions

| Component | Version | Purpose |
|-----------|---------|---------|
| **Ollama Server** | **v0.12.10** | **LLM inference server (bundled)** |
| **ollama-python** | **v0.6.0** | **Python client for Ollama** |
| Python | 3.14.0 | Runtime (bundled with PyInstaller) |
| Pydantic AI | 1.12.0 | Orchestrator/router framework |
| Pydantic | 2.12.4 | JSON validation |
| FastAPI | 0.115.0 | Backend API framework |
| Appscript | 1.4.0 | macOS automation (Apple Events) |
| PyInstaller | 6.16.0 | Python backend bundling |
| Tauri | 2.9.x | Desktop app framework |
| Rust | 1.91.1 | Tauri backend language |
| Node.js | 25.1.0 | Frontend build tooling |
| React | 19.2.0 | Frontend UI framework |
| TypeScript | 5.9.3 | Frontend type safety |
| Tailwind CSS | 4.1.17 | Frontend styling |

---

## 2. Executive Summary

Phase 1.1 establishes the foundational architecture for Baby AI's Python rewrite, validating the complete end-to-end command chain: natural language input → LLM planning → tool execution → natural language response. This phase implements only the **App Agent** domain (macOS application control) to prove the architecture before scaling to all 10 domains.

**Key Objectives:**
- Validate LLM function calling with Pydantic AI orchestration
- Demonstrate robust error handling (app not found scenarios)
- Establish model-agnostic architecture (LLM and embeddings)
- Deliver natural language UX (friendly error messages)
- Create standalone DMG package with bundled Python 3.14 backend and Ollama Server v0.12.10

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Input                            │
│                  (Natural Language)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            Pydantic AI Orchestrator                   │   │
│  │  - Validates LLM JSON output                         │   │
│  │  - Manages retry logic                               │   │
│  │  - Routes to domain agents                           │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LLM Client (Abstract)                    │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │         Ollama Adapter (Phase 1.1)             │  │   │
│  │  │  - Mistral 7B Instruct                         │  │   │
│  │  │  - Function calling JSON generation            │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │      Future: Gemini/Claude Adapters            │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              App Agent (Domain)                       │   │
│  │  - open_app(appName: str)                            │   │
│  │  - close_app(appName: str)                           │   │
│  │  - Try/except error handling                         │   │
│  │  - Appscript execution                               │   │
│  └────────────┬─────────────────────────────────────────┘   │
│               │                                              │
└───────────────┼──────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│                    macOS System                              │
│              (Appscript → Apple Events)                      │
└─────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Natural Language Response                   │
│         (Success or friendly error message)                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Tauri Desktop Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Tauri Desktop App (Rust)                     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Frontend (React + TypeScript + Tailwind)          │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │           ChatPage (Minimal UI)                     │ │ │
│  │  │  - Message input/output                             │ │ │
│  │  │  - Streaming response display                       │ │ │
│  │  │  - Send button                                      │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │                                                           │ │
│  │  HTTP POST /api/chat → http://localhost:8000            │ │
│  └───────────────────────────┬───────────────────────────────┘ │
│                              │                                 │
│  ┌───────────────────────────▼───────────────────────────────┐ │
│  │         Tauri Backend Manager (Rust)                      │ │
│  │  - Launches Python FastAPI backend on startup            │ │
│  │  - Launches Ollama service                               │ │
│  │  - Health checks for both services                       │ │
│  │  - Native OS integration (notifications, windows)        │ │
│  └───────────────────────────┬───────────────────────────────┘ │
│                              │                                 │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              Python FastAPI Backend (Port 8000)                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │            Pydantic AI Orchestrator                       │   │
│  │  - Validates LLM JSON output                            │   │
│  │  - Manages retry logic                                  │   │
│  │  - Routes to domain agents                              │   │
│  └────────────┬─────────────────────────────────────────────┘   │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              LLM Client (Abstract)                        │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │         Ollama Adapter (Phase 1.1)                 │  │   │
│  │  │  - Mistral 7B Instruct                            │  │   │
│  │  │  - Function calling JSON generation               │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └────────────┬─────────────────────────────────────────────┘   │
│               │                                                 │
│               ▼                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              App Agent (Domain)                           │   │
│  │  - open_app(appName: str)                                │   │
│  │  - close_app(appName: str)                               │   │
│  │  - Appscript execution                                   │   │
│  └────────────┬─────────────────────────────────────────────┘   │
│               │                                                 │
└───────────────┼──────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Ollama Service (Port 11434)                    │
│              Mistral 7B Instruct + nomic-embed-text             │
└─────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    macOS System                                 │
│              (Appscript → Apple Events)                         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Component Responsibilities

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Tauri Desktop App** | Desktop wrapper, launches backend/Ollama, native OS integration | Rust + Tauri v2.9.x |
| **React Frontend** | Minimal ChatPage UI for testing | React 19 + TypeScript + Tailwind CSS |
| **FastAPI Backend** | REST API endpoints, request/response handling | FastAPI 0.115.0 |
| **Pydantic AI Orchestrator** | Routing, validation, retry logic | Pydantic AI v1.12.0 |
| **LLM Client (Abstract)** | Model-agnostic interface for LLM calls | Python ABC |
| **Ollama Adapter** | Concrete implementation for Ollama | Ollama Python Client |
| **App Agent** | macOS app control (open/close) via Appscript | Appscript v1.4.0 |

**Note on PyObjC:** PyObjC is reserved for future phases (Window Agent, System Agent, Vision Agent) for low-level macOS framework access (CoreGraphics, Vision, etc.). Phase 1.1 uses only Appscript for high-level application control.

---

## 3. Data Models (Pydantic Schemas)

### 3.1 Core Models

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any
from datetime import datetime

class ToolCall(BaseModel):
    """Represents a function call from the LLM"""
    /* Lines 219-221 omitted */
    function: FunctionCall

class FunctionCall(BaseModel):
    """Function name and arguments"""
    /* Lines 225-226 omitted */
    arguments: Dict[str, Any] = Field(description="Function arguments as dict")

class ExecutionResult(BaseModel):
    """Result of tool execution"""
    /* Lines 230-233 omitted */
    duration_ms: float = Field(description="Execution time in milliseconds")
    
class AgentTrace(BaseModel):
    """Telemetry and logging data"""
    /* Lines 237-243 omitted */
    confidence: Optional[float] = Field(default=None, description="LLM confidence score")

class ChatRequest(BaseModel):
    """User request to the API"""
    /* Lines 247-249 omitted */
    stream: bool = Field(default=False, description="Enable streaming response")

class ChatResponse(BaseModel):
    """Response from the API"""
    /* Lines 253-256 omitted */
    trace: Optional[AgentTrace] = Field(default=None, description="Execution trace")

class ChatChunk(BaseModel):
    """Streaming response chunk"""
    /* Lines 260-264 omitted */
    usage: Optional[Dict[str, int]] = Field(default=None, description="Token usage (final chunk only)")
```

### 3.2 LLM Client Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMClient(ABC):
    """Abstract interface for LLM providers"""

class OllamaAdapter(LLMClient):
    """Ollama implementation of LLM client"""
```

---

## 4. App Agent Implementation

### 4.1 Tool Definitions

```python
from appscript import app as appscript_app
import time

class AppAgent:
    """Agent for macOS application control"""
```

---

## 5. Orchestrator Logic

### 5.1 System Prompt

```python
SYSTEM_PROMPT = """You are an intelligent macOS automation assistant powered by Baby AI.

Your primary role is Function Calling:
1. Analyze the user's request
2. Generate JSON function calls using the available tools
3. After the tool executes, you will receive a status message (success or error)
4. Reformulate the status message into natural, friendly language for the user

Communication Guidelines:
- Use conversational, friendly tone
- Avoid technical jargon and programming terms
- If an error occurs, explain it in simple terms
- Be concise but helpful

Available domains in this phase: App (application control)

Example interactions:
User: "Open Spotify"
You: [Generate open_app function call]
System: [Returns "Application 'Spotify' activated successfully"]
You: "I've opened Spotify for you!"

User: "Close Chrome"
You: [Generate close_app function call]
System: [Returns error "Application 'Chrome' not found"]
You: "I tried to close Chrome, but it doesn't seem to be installed on your Mac."
"""
```

### 5.2 Retry Logic

```python
class OrchestratorConfig(BaseModel):
    """Configuration for orchestrator behavior"""
    /* Lines 552-555 omitted */
    llm_timeout_seconds: int = 30

async def orchestrate_with_retry(
    user_message: str,
    /* Lines 559-561 omitted */
    conversation_id: Optional[str] = None
) -> ChatResponse:
    """
```

---

## 6. FastAPI Endpoints

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Baby AI Backend", version="1.1.0")

# CORS for Tauri frontend
app.add_middleware(
    CORSMiddleware,
    /* Lines 672-675 omitted */
    allow_headers=["*"],
)
