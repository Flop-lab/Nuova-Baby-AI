# Baby AI - Phase 1.1 Implementation Plan
## App Agent POC - Step-by-Step Execution Plan

**Version:** 1.1  
**Date:** November 10, 2025  
**Status:** Ready for Execution

---

## Versions

### Ollama Versions (IMPORTANT: Two Different Components)

**Ollama Server** (macOS binary to bundle with Tauri):
- **Version:** v0.12.10
- **Source:** https://github.com/ollama/ollama/releases
- **Purpose:** Local LLM inference server (bundled in Phase 1.1)

**ollama-python SDK** (Python client library):
- **Version:** v0.6.0
- **Source:** https://github.com/ollama/ollama-python/releases
- **Purpose:** Python API client to communicate with Ollama server
- **Installation:** `pip install ollama==0.6.0` (in requirements.txt)

**Note:** These two components have **independent versioning**. The server is at v0.12.10 while the Python SDK is at v0.6.0. Both are the latest stable versions as of November 2025.

### All Component Versions

| Component | Version | Purpose |
|-----------|---------|---------|
| **Ollama Server** | **v0.12.10** | **LLM inference server (bundled)** |
| **ollama-python** | **v0.6.0** | **Python client for Ollama** |
| Python | 3.14.0 | Runtime (bundled with PyInstaller) |
| Pydantic AI | 1.12.0 | Orchestrator/router framework |
| Pydantic | 2.12.4 | JSON validation |
| FastAPI | 0.115.0 | Backend API framework |
| Appscript | 1.4.0 | macOS automation (Apple Events) |
| PyInstaller | 6.11.1 | Python backend bundling |
| Tauri | 2.9.x | Desktop app framework |
| Rust | 1.91.1 | Tauri backend language |
| Node.js | 25.1.0 | Frontend build tooling |
| React | 19.2.0 | Frontend UI framework |
| TypeScript | 5.9.3 | Frontend type safety |
| Tailwind CSS | 4.1.17 | Frontend styling |

---

## Overview

This document provides a detailed, step-by-step implementation plan for Phase 1.1 of the Baby AI Python rewrite. The plan is designed to be executed sequentially, with clear checkpoints and validation at each step.

**Estimated Time:** 3 days  
**Prerequisites:** macOS with Python 3.14, Ollama Server v0.12.10 installed, Qwen3-4B-Thinking-2507-Q8_0 model pulled, Node.js 25 (via nvm), Rust 1.91.1 for Tauri

---

## Directory Structure

```
baby-ai-python/
├── src/                           # Python backend
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration and env vars
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py             # Pydantic models (ToolCall, ExecutionResult, etc.)
│   │   └── config.py              # OrchestratorConfig
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py              # LLMClient abstract interface
│   │   └── ollama_adapter.py      # OllamaAdapter implementation
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py                # BaseAgent abstract class
│   │   └── app_agent.py           # AppAgent implementation
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   ├── prompts.py             # System prompts
│   │   └── orchestrator.py        # Main orchestration logic
│   └── utils/
│       ├── __init__.py
│       └── logger.py              # Structured logging setup
├── src-tauri/                     # Tauri desktop app
│   ├── src/
│   │   ├── main.rs                # Rust main process
│   │   └── backend_manager.rs     # Python backend + Ollama launcher
│   ├── Cargo.toml
│   └── tauri.conf.json
├── ui/                            # Frontend (HTML/JS/CSS)
│   ├── index.html                 # Chat UI
│   ├── styles.css
│   └── app.js                     # Frontend logic
├── tests/
│   ├── __init__.py
│   ├── test_app_agent.py
│   ├── test_ollama_adapter.py
│   ├── test_orchestrator.py
│   └── test_integration.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── pyproject.toml                 # Optional: for Poetry users
```

---

## Implementation Steps

### Phase 0: Environment Setup (30 minutes) ✅ COMPLETED

#### Step 0.1: Create Project Directory
```bash
# Navigate to your development folder, for example:
cd ~/Developer 
# Create the project directory and navigate into it
mkdir -p "Nuova Baby AI"
cd "Nuova Baby AI"
```

#### Step 0.2: Initialize Git (on NEWBABY7 branch)
```bash
git checkout NEWBABY7
git pull origin NEWBABY7
```

#### Step 0.3: Create Python Virtual Environment
```bash
python3.14 -m venv venv
source venv/bin/activate
python --version  # Verify 3.14.x
```

#### Step 0.4: Install Dependencies
```bash
cp /home/ubuntu/requirements.txt .
pip install --upgrade pip
pip install -r requirements.txt
```

**Validation:**
- [ ] Python 3.14.x confirmed
- [ ] All packages installed without errors
- [ ] `python -c "import pydantic_ai; print(pydantic_ai.__version__)"` shows 1.12.0

#### Step 0.5: Verify Ollama
```bash
ollama --version
ollama list | grep qwen3
```

**Expected:** Qwen3-4B-Thinking-2507-Q8_0 model present

**If missing:**
```bash
ollama pull qwen3:4b-thinking-2507-q8_0
ollama pull nomic-embed-text
```

---

### Phase 1: Core Data Models (1 hour) ✅ COMPLETED

#### Step 1.1: Create Project Structure
```bash
mkdir -p src/{models,llm,agents,orchestrator,utils}
mkdir -p tests
touch src/__init__.py
touch src/models/__init__.py
touch src/llm/__init__.py
touch src/agents/__init__.py
touch src/orchestrator/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py
```

#### Step 1.2: Implement Pydantic Schemas (`src/models/schemas.py`)

**Content:**
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any, List
from datetime import datetime

class FunctionCall(BaseModel):
    """Function name and arguments"""
    /* Lines 186-187 omitted */
    arguments: Dict[str, Any] = Field(description="Function arguments as dict")

class ToolCall(BaseModel):
    """Represents a function call from the LLM"""
    /* Lines 191-193 omitted */
    function: FunctionCall

class ExecutionResult(BaseModel):
    """Result of tool execution"""
    /* Lines 197-200 omitted */
    duration_ms: float = Field(description="Execution time in milliseconds")

class AgentTrace(BaseModel):
    """Telemetry and logging data"""
    /* Lines 204-210 omitted */
    confidence: Optional[float] = Field(default=None, description="LLM confidence score")

class ChatRequest(BaseModel):
    """User request to the API"""
    /* Lines 214-216 omitted */
    stream: bool = Field(default=False, description="Enable streaming response")

class ChatResponse(BaseModel):
    """Response from the API"""
    /* Lines 220-223 omitted */
    trace: Optional[AgentTrace] = Field(default=None, description="Execution trace")

class ChatChunk(BaseModel):
    """Streaming response chunk"""
    /* Lines 227-231 omitted */
    usage: Optional[Dict[str, int]] = Field(default=None)
```

**Validation:**
```bash
python -c "from src.models.schemas import ChatRequest, ChatResponse; print('✅ Schemas OK')"
```

#### Step 1.3: Implement Orchestrator Config (`src/models/config.py`)

**Content:**
```python
from pydantic import BaseModel, Field

class OrchestratorConfig(BaseModel):
    """Configuration for orchestrator behavior"""
    /* Lines 247-250 omitted */
    llm_timeout_seconds: int = Field(default=30, description="LLM request timeout")
```

**Validation:**
```bash
python -c "from src.models.config import OrchestratorConfig; c = OrchestratorConfig(); print(f'✅ Config OK: {c.max_validation_retries} retries')"
```

---

### Phase 2: LLM Client Layer (2 hours) ✅ COMPLETED

#### Step 2.1: Create Abstract LLM Client (`src/llm/client.py`)

**Content:**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMClient(ABC):
    """Abstract interface for LLM providers"""
```

**Validation:**
```bash
python -c "from src.llm.client import LLMClient; print('✅ LLMClient interface OK')"
```

#### Step 2.2: Implement Ollama Adapter (`src/llm/ollama_adapter.py`)

**Content:**
```python
import ollama
from typing import List, Dict, Any, Optional
from src.llm.client import LLMClient
import structlog

logger = structlog.get_logger()

class OllamaAdapter(LLMClient):
    """Ollama implementation of LLM client"""
```

**Validation:**
```bash
# Create test script
cat > test_ollama.py << 'EOF'
import asyncio
from src.llm.ollama_adapter import OllamaAdapter

async def test():
    adapter = OllamaAdapter()
    /* Lines 491-495 omitted */
    print(f"✅ Ollama test OK: {result['content'][:50]}")

asyncio.run(test())
EOF

python test_ollama.py
rm test_ollama.py
```

---

### Phase 3: App Agent Implementation (2 hours) ✅ COMPLETED

#### Step 3.1: Create Base Agent (`src/agents/base.py`)

**Content:**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.schemas import ToolCall, ExecutionResult

class BaseAgent(ABC):
    """Base class for all domain agents"""
```

#### Step 3.2: Implement App Agent (`src/agents/app_agent.py`)

**Content:**
```python
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
```

**Validation:**
```bash
# Test AppAgent tools definition
python -c "from src.agents.app_agent import AppAgent; tools = AppAgent.get_tools(); print(f'✅ AppAgent OK: {len(tools)} tools defined')"
```

---

### Phase 4: Orchestrator Logic (3 hours) ✅ COMPLETED

#### Step 4.1: Create System Prompts (`src/orchestrator/prompts.py`)

**Content:**
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
You: [Generate open_app function call with appName: "Spotify"]
System: [Returns "Application 'Spotify' activated successfully"]
You: "I've opened Spotify for you!"

User: "Close Chrome"
You: [Generate close_app function call with appName: "Chrome"]
System: [Returns error "Application 'Chrome' not found"]
You: "I tried to close Chrome, but it doesn't seem to be installed on your Mac."

Remember: Always use the exact parameter name "appName" (not "app" or other variations).
"""
```

#### Step 4.2: Implement Orchestrator (`src/orchestrator/orchestrator.py`)

**Content:**
```python
import asyncio
import uuid
from typing import Optional
from pydantic import ValidationError
from src.llm.client import LLMClient
from src.agents.app_agent import AppAgent
from src.models.schemas import ChatRequest, ChatResponse, ToolCall, AgentTrace
from src.models.config import OrchestratorConfig
from src.orchestrator.prompts import SYSTEM_PROMPT
import structlog

logger = structlog.get_logger()

async def orchestrate_with_retry(
    user_message: str,
    /* Lines 741-743 omitted */
    conversation_id: Optional[str] = None
) -> ChatResponse:
    """
    /* Lines 746-900 omitted */
    )
```

---

### Phase 5: FastAPI Backend (2 hours) ✅ COMPLETED

#### Step 5.1: Setup Logging (`src/utils/logger.py`)

**Content:**
```python
import structlog
import logging

def setup_logging():
    """Configure structured logging"""
    /* Lines 916-937 omitted */
    )
```

#### Step 5.2: Configuration (`src/config.py`)

**Content:**
```python
import os
from pydantic import BaseModel

class Settings(BaseModel):
    """Application settings"""
    /* Lines 949-959 omitted */
    cors_origins: list = ["*"]  # TODO: Restrict in production

settings = Settings()
```

#### Step 5.3: Main FastAPI App (`src/main.py`)

**Content:**
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from typing import Optional
import structlog

from src.config import settings
from src.models.schemas import ChatRequest, ChatResponse, ChatChunk
from src.models.config import OrchestratorConfig
from src.llm.ollama_adapter import OllamaAdapter
from src.llm.client import LLMClient
from src.orchestrator.orchestrator import orchestrate_with_retry
from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Global instances
llm_client: Optional[LLMClient] = None
orchestrator_config = OrchestratorConfig()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    /* Lines 994-1012 omitted */
    logger.info("Baby AI backend shutting down")

app = FastAPI(
    title="Baby AI Backend",
    /* Lines 1016-1017 omitted */
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    /* Lines 1023-1026 omitted */
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    /* Lines 1032-1037 omitted */
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint with optional streaming support"""

async def stream_chat_response(request: ChatRequest):
    """Stream chat response as NDJSON chunks"""
    /* Lines 1076-1108 omitted */
    yield json.dumps(final_chunk.dict()) + "\n"

if __name__ == "__main__":
    import uvicorn
    /* Lines 1112-1117 omitted */
    )
```

#### Step 5.4: Create .env.example

**Content:**
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen3:4b-thinking-2507-q8_0
EMBED_MODEL=nomic-embed-text

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**Validation:**
```bash
# Test server startup
python -m src.main &
sleep 5
curl http://localhost:8000/health
# Should return: {"status":"healthy","llm_initialized":true,"version":"1.1.0"}
pkill -f "python -m src.main"
```

---


### Phase 6: Testing (3 hours) ✅ COMPLETED

**Results:** 17/17 tests PASSED, 44% coverage achieved
- AppAgent: 90% coverage
- Schemas: 100% coverage  
- LLM Client: 83% coverage
- Integration tests: All core flows tested

**Test Execution:**
```bash
# Run all tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Results: 17 passed, coverage 44%
```

#### Step 6.1: Unit Tests for App Agent (`tests/test_app_agent.py`) ✅

**Content:**
```python
import pytest
from src.agents.app_agent import AppAgent
from src.models.schemas import ToolCall, FunctionCall

@pytest.mark.asyncio
async def test_app_agent_tools():
    """Test that AppAgent returns correct tool definitions"""
    tools = AppAgent.get_tools()
    assert len(tools) == 2
    assert tools[0]["function"]["name"] == "open_app"
    assert tools[1]["function"]["name"] == "close_app"
    
    # Verify strict schema
    open_params = tools[0]["function"]["parameters"]
    assert "appName" in open_params["properties"]
    assert open_params["additionalProperties"] == False
    assert open_params["required"] == ["appName"]

@pytest.mark.asyncio
async def test_app_agent_friendly_error():
    """Test that app not found returns friendly error"""
    agent = AppAgent()
    
    tool_call = ToolCall(
        id="test-1",
        type="function",
        function=FunctionCall(
            name="open_app",
            arguments={"appName": "NonExistentApp12345"}
        )
    )
    
    result = await agent.execute(tool_call)
    
    assert result.success == False
    assert "doesn't seem to be installed" in result.message
    assert "NonExistentApp12345" in result.message
```

#### Step 6.2: Integration Tests (`tests/test_integration.py`)

**Content:**
```python
import pytest
from src.llm.ollama_adapter import OllamaAdapter
from src.orchestrator.orchestrator import orchestrate_with_retry
from src.models.config import OrchestratorConfig

@pytest.mark.asyncio
async def test_end_to_end_valid_app():
    """Test full flow with a valid app (TextEdit should exist on macOS)"""
    llm_client = OllamaAdapter()
    config = OrchestratorConfig()
    
    response = await orchestrate_with_retry(
        user_message="Open TextEdit",
        llm_client=llm_client,
        config=config
    )
    
    assert response.message is not None
    assert len(response.message) > 0
    # Should have trace if tool was called
    if response.trace:
        assert response.trace.agent_name == "AppAgent"
        assert response.trace.domain == "app"

@pytest.mark.asyncio
async def test_end_to_end_invalid_app():
    """Test full flow with invalid app"""
    llm_client = OllamaAdapter()
    config = OrchestratorConfig()
    
    response = await orchestrate_with_retry(
        user_message="Open FakeApp999",
        llm_client=llm_client,
        config=config
    )
    
    assert response.message is not None
    # Should contain friendly error message
    assert "doesn't seem to be installed" in response.message.lower() or \
           "not found" in response.message.lower()
```

#### Step 6.3: Streaming Tests (`tests/test_streaming.py`)

**Content:**
```python
import pytest
from src.llm.ollama_adapter import OllamaAdapter
from src.models.schemas import ChatChunk

@pytest.mark.asyncio
async def test_ollama_stream():
    """Test that OllamaAdapter.stream() yields ChatChunk objects"""
    llm_client = OllamaAdapter()
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello"}
    ]
    
    chunks = []
    async for chunk in llm_client.stream(messages=messages, tools=[]):
        assert isinstance(chunk, ChatChunk)
        assert chunk.type in ["delta", "final"]
        chunks.append(chunk)
    
    # Should have at least one delta chunk and one final chunk
    assert len(chunks) >= 2
    assert chunks[-1].type == "final"

@pytest.mark.asyncio
async def test_stream_ndjson_format():
    """Test that streaming endpoint returns valid NDJSON"""
    from fastapi.testclient import TestClient
    from src.main import app
    
    client = TestClient(app)
    
    response = client.post(
        "/api/chat",
        json={"message": "Say hello", "stream": True}
    )
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/x-ndjson"
    
    lines = response.text.strip().split("\n")
    assert len(lines) >= 2  # At least meta and final chunks
    
    # Parse first chunk (meta)
    import json
    meta_chunk = json.loads(lines[0])
    assert meta_chunk["type"] == "meta"
    assert "conversation_id" in meta_chunk
    assert "step_id" in meta_chunk
    
    # Parse last chunk (final)
    final_chunk = json.loads(lines[-1])
    assert final_chunk["type"] == "final"
```

#### Step 6.4: Run Tests

**Commands:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Expected: >90% coverage
```

---

### Phase 7: Manual Testing & Validation (1 hour)

#### Step 7.1: Start Server
```bash
python -m src.main
```

#### Step 7.2: Test with curl

**Test 1: Valid app (TextEdit)**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open TextEdit"}'
```

**Expected:** Friendly response like "I've opened TextEdit for you!"

**Test 2: Invalid app**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open FakeApp123"}'
```

**Expected:** Friendly error like "I tried to open FakeApp123, but it doesn't seem to be installed on your system."

**Test 3: Close app**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Close TextEdit"}'
```

**Expected:** Confirmation message

**Test 4: Streaming mode**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Say hello", "stream": true}'
```

**Expected:** NDJSON chunks (meta → delta → final)

**Test 5: Conversation tracking**
```bash
# First message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Open TextEdit"}'

# Copy conversation_id from response, then send second message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Close it", "conversation_id": "PASTE_CONVERSATION_ID_HERE"}'
```

**Expected:** Same conversation_id in both responses, different step_id

#### Step 7.3: Validation Checklist

- [ ] App not installed returns friendly error (no crash)
- [ ] Valid function calling (LLM generates valid JSON)
- [ ] Validation retry works (check logs for retry attempts if needed)
- [ ] Only open_app and close_app are callable
- [ ] Natural language responses (no technical jargon)
- [ ] Logging includes agent_name, domain, step_id, result
- [ ] Streaming mode returns NDJSON chunks (meta → delta → final)
- [ ] Non-streaming mode returns complete JSON response
- [ ] Conversation tracking persists conversation_id across turns
- [ ] Step tracking generates unique step_id per turn
- [ ] End-to-end latency < 3 seconds (p95) on warm LLM

---

### Phase 8: Documentation (1 hour)

#### Step 8.1: Create README.md

**Content:**
```markdown
# Baby AI - Phase 1.1 POC

Python rewrite of Baby AI with multi-agent architecture. Phase 1.1 implements the App Agent for macOS application control.

## Prerequisites

- macOS 13+ (Ventura or later)
- Python 3.14.0 (or 3.12+ as fallback)
- Ollama installed locally
- Qwen3-4B-Thinking-Q8_0

## Setup

1. **Install Ollama**
   ```bash
   # Download from https://ollama.ai
   ollama --version
   ```

2. **Pull Models**
   ```bash
   ollama pull qwen3:4b-thinking-2507-q8_0
   ollama pull nomic-embed-text
   ```

3. **Create Virtual Environment**
   ```bash
   python3.14 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

## Running

```bash
# Start server
python -m src.main

# Server runs on http://localhost:8000
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## API Usage

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "Open Spotify"
}
```

**Response:**
```json
{
  "message": "I've opened Spotify for you!",
  "conversation_id": "uuid-here",
  "trace": {
    "agent_name": "AppAgent",
    "domain": "app",
    "step_id": "uuid-here",
    "tool_call": {...},
    "result": {...}
  }
}
```

## Architecture

- **FastAPI Backend**: REST API server
- **Pydantic AI**: Orchestration and routing
- **LLM Client**: Model-agnostic interface (Ollama adapter)
- **App Agent**: macOS app control (open/close)

## Phase 1.1 Scope

- ✅ App Agent only (open_app, close_app)
- ✅ Validation retry (3 attempts max)
- ✅ Friendly error messages
- ✅ Structured logging
- ⏭️ Warm-up (Phase 1.2)
- ⏭️ Other agents (Phase 1.2+)

## License

[Your license here]
```

#### Step 8.2: Create .gitignore

**Content:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

---

### Phase 9: Tauri Integration & Binary Management (3 hours)

#### Step 9.1: Initialize Tauri Project

**Commands:**
```bash
cd baby-ai-python

# Ensure Rust 1.91.1 is installed
rustup update
rustc --version  # Should show 1.91.1

# Install Tauri CLI v2
cargo install tauri-cli --version ^2.0

# Initialize Tauri v2 (if not already initialized)
cargo tauri init
```

**Note:** This uses Tauri v2.9.x which requires Rust 1.91.1 and has breaking changes from v1.x (new API imports, capabilities model).

**Configuration prompts:**
- App name: Baby AI
- Window title: Baby AI
- Web assets: `../ui`
- Dev server URL: `http://localhost:8000` (for dev mode)
- Before dev command: (leave empty)
- Before build command: (leave empty)

#### Step 9.2: Create Backend Manager (`src-tauri/src/backend_manager.rs`)

**Content:**
```rust
use std::process::{Command, Child, Stdio};
use std::path::PathBuf;
use std::fs;

pub struct BackendManager {
    python_process: Option<Child>,
    ollama_process: Option<Child>,
}

impl BackendManager {
    pub fn new() -> Self {
        BackendManager {
            python_process: None,
            ollama_process: None,
        }
    }
    
    pub fn start_ollama(&mut self) -> Result<(), String> {
        // Check if Ollama is already running
        let status = Command::new("curl")
            .args(&["-s", "http://localhost:11434/api/version"])
            .output();
        
        if status.is_ok() && status.unwrap().status.success() {
            println!("Ollama already running");
            return Ok(());
        }
        
        // Start Ollama server with fallback logic
        println!("Starting Ollama server...");
        
        // Try system Ollama first, then bundled binary
        let ollama_child = self.try_start_system_ollama()
            .or_else(|e| {
                eprintln!("System Ollama failed: {}. Trying bundled binary...", e);
                self.try_start_bundled_ollama()
            })
            .map_err(|e| format!("Failed to start Ollama (system and bundled): {}", e))?;
        
        self.ollama_process = Some(ollama_child);
        
        // Wait for Ollama to be ready (max 10 seconds)
        for _ in 0..20 {
            std::thread::sleep(std::time::Duration::from_millis(500));
            let check = Command::new("curl")
                .args(&["-s", "http://localhost:11434/api/version"])
                .output();
            
            if check.is_ok() && check.unwrap().status.success() {
                println!("Ollama ready");
                return Ok(());
            }
        }
        
        Err("Ollama failed to start within 10 seconds".to_string())
    }
    
    fn try_start_system_ollama(&self) -> Result<Child, String> {
        // Attempt 1: Use system Ollama (in $PATH)
        println!("Attempting to start system Ollama...");
        Command::new("ollama")
            .arg("serve")
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .map_err(|e| format!("System Ollama not found: {}", e))
    }
    
    fn try_start_bundled_ollama(&self) -> Result<Child, String> {
        // Attempt 2: Use bundled Ollama Server v0.12.10
        println!("Attempting to start bundled Ollama Server v0.12.10...");
        
        let bundled_path = self.get_bundled_ollama_path()?;
        
        if !bundled_path.exists() {
            return Err(format!("Bundled Ollama not found at: {:?}", bundled_path));
        }
        
        println!("Launching bundled Ollama: {:?}", bundled_path);
        Command::new(&bundled_path)
            .arg("serve")
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .map_err(|e| format!("Failed to start bundled Ollama: {}", e))
    }
    
    fn get_bundled_ollama_path(&self) -> Result<PathBuf, String> {
        // Determine architecture-specific binary name
        let arch = std::env::consts::ARCH;
        let binary_name = match arch {
            "aarch64" => "ollama-darwin-arm64",
            "x86_64" => "ollama-darwin-amd64",
            _ => return Err(format!("Unsupported architecture: {}", arch)),
        };
        
        // In production, binaries are in the app bundle's Resources directory
        // In development, they're in src-tauri/binaries
        let exe_dir = std::env::current_exe()
            .map_err(|e| format!("Failed to get exe dir: {}", e))?
            .parent()
            .ok_or("No parent dir")?
            .to_path_buf();
        
        // Try production path first (macOS app bundle)
        let production_path = exe_dir.join("../Resources").join(binary_name);
        if production_path.exists() {
            return Ok(production_path);
        }
        
        // Fallback to development path
        let dev_path = PathBuf::from("src-tauri/binaries").join(binary_name);
        if dev_path.exists() {
            return Ok(dev_path);
        }
        
        Err(format!("Bundled Ollama binary '{}' not found", binary_name))
    }
    
    pub fn start_python_backend(&mut self) -> Result<(), String> {
        println!("Starting Python backend...");
        
        // Get the path to the Python backend
        let backend_path = self.get_backend_path()?;
        
        // Try to launch bundled backend first, fallback to system Python in debug mode
        let backend_binary = backend_path.join("dist").join("babyai-backend").join("babyai-backend");
        
        let python_child = if backend_binary.exists() {
            // Production mode: use bundled backend
            println!("Launching bundled backend: {:?}", backend_binary);
            Command::new(&backend_binary)
                .current_dir(&backend_path)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .map_err(|e| format!("Failed to start bundled backend: {}", e))?
        } else if cfg!(debug_assertions) {
            // Development mode: use system Python
            println!("Launching backend with system Python (dev mode)");
            let python_bin = std::env::var("BABYAI_PYTHON_BIN")
                .unwrap_or_else(|_| "python3.14".to_string());
            
            Command::new(&python_bin)
                .args(&["-m", "uvicorn", "src.main:app", "--host", "127.0.0.1", "--port", "8000"])
                .current_dir(&backend_path)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .map_err(|e| format!("Failed to start Python backend: {}", e))?
        } else {
            return Err("Bundled backend not found and not in debug mode".to_string());
        };
        
        self.python_process = Some(python_child);
        
        // Wait for backend to be ready (max 10 seconds)
        for _ in 0..20 {
            std::thread::sleep(std::time::Duration::from_millis(500));
            let check = Command::new("curl")
                .args(&["-s", "http://127.0.0.1:8000/health"])
                .output();
            
            if check.is_ok() && check.unwrap().status.success() {
                println!("Python backend ready");
                return Ok(());
            }
        }
        
        Err("Python backend failed to start within 10 seconds".to_string())
    }
    
    fn get_backend_path(&self) -> Result<PathBuf, String> {
        // In development: use the local path
        // In production: use the bundled path
        let dev_path = PathBuf::from(".");
        
        if dev_path.join("src").join("main.py").exists() {
            Ok(dev_path)
        } else {
            Err("Backend path not found".to_string())
        }
    }
    
    pub fn shutdown(&mut self) {
        println!("Shutting down backend services...");
        
        if let Some(mut child) = self.python_process.take() {
            let _ = child.kill();
        }
        
        // Don't kill Ollama if it was already running
        // Only kill if we started it
        if let Some(mut child) = self.ollama_process.take() {
            let _ = child.kill();
        }
    }
}

impl Drop for BackendManager {
    fn drop(&mut self) {
        self.shutdown();
    }
}
```

#### Step 9.3: Update Tauri Main (`src-tauri/src/main.rs`)

**Content:**
```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod backend_manager;

use backend_manager::BackendManager;
use std::sync::Mutex;
use tauri::State;

struct AppState {
    backend: Mutex<BackendManager>,
}

#[tauri::command]
fn check_backend_status() -> Result<String, String> {
    // Check if backend is responding
    let output = std::process::Command::new("curl")
        .args(&["-s", "http://127.0.0.1:8000/health"])
        .output()
        .map_err(|e| format!("Failed to check backend: {}", e))?;
    
    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err("Backend not responding".to_string())
    }
}

fn main() {
    let mut backend_manager = BackendManager::new();
    
    // Start Ollama
    if let Err(e) = backend_manager.start_ollama() {
        eprintln!("Warning: {}", e);
    }
    
    // Start Python backend
    if let Err(e) = backend_manager.start_python_backend() {
        eprintln!("Error starting backend: {}", e);
        std::process::exit(1);
    }
    
    tauri::Builder::default()
        .manage(AppState {
            backend: Mutex::new(backend_manager),
        })
        .invoke_handler(tauri::generate_handler![check_backend_status])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#### Step 9.4: Update Cargo.toml

Add dependencies:
```toml
[dependencies]
tauri = { version = "1.5", features = ["shell-open"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
```

**Validation:**
```bash
cd src-tauri
cargo build
# Should compile without errors
```

---

### Phase 9.5: Python Backend Bundling & Ollama Server Integration (2 hours)

**Goal:** Bundle the Python backend into a standalone executable using PyInstaller AND integrate Ollama Server v0.12.10 binary, enabling the app to run without requiring Python or Ollama installation on the user's system.

#### Step 9.5.1: Create Python Entrypoint Script

**File:** `src/backend_entry.py`

**Content:**
```python
"""
Backend entrypoint for bundled executable.
This script programmatically starts the FastAPI server using uvicorn.
"""
import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
```

**Why:** PyInstaller works better with a direct Python entrypoint than with `python -m uvicorn`. This ensures all imports are tracked correctly.

#### Step 9.5.2: Add PyInstaller to Requirements

**File:** `requirements.txt`

Add:
```
# ============================================================================
# Bundling (Production)
# ============================================================================
pyinstaller== ultima versione
```

**Install:**
```bash
cd baby-ai-python
source venv/bin/activate
pip install pyinstaller==6.11.1
```

#### Step 9.5.3: Create PyInstaller Spec File

**File:** `baby-ai-backend.spec`

**Content:**
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/backend_entry.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'pydantic_ai',
        'pydantic_ai.models',
        'pydantic_ai.models.ollama',
        'ollama',
        'appscript',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='babyai-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='babyai-backend',
)
```

**Why:** The spec file tells PyInstaller:
- Entry point: `src/backend_entry.py`
- Hidden imports: uvicorn, pydantic-ai, ollama, appscript (dynamic imports)
- Output: `dist/babyai-backend/babyai-backend` (onedir mode for easier debugging)

#### Step 9.5.4: Build Backend Executable

**Commands:**
```bash
cd baby-ai-python
source venv/bin/activate

# Build with PyInstaller
pyinstaller baby-ai-backend.spec

# Verify the executable was created
ls -lh dist/babyai-backend/babyai-backend
```

**Expected Output:**
```
dist/
└── babyai-backend/
    ├── babyai-backend          # Main executable
    ├── _internal/              # Python runtime + dependencies
    └── ...
```

**Validation:**
```bash
# Test the bundled backend directly
cd baby-ai-python
./dist/babyai-backend/babyai-backend

# In another terminal, test the API
curl http://127.0.0.1:8000/health
# Should return: {"status":"healthy"}

# Stop the backend (Ctrl+C)
```

#### Step 9.5.5: Update Tauri to Use Bundled Backend

The dual-mode launcher in `backend_manager.rs` (Step 9.2) already checks for the bundled backend:

```rust
let backend_binary = backend_path.join("dist").join("babyai-backend").join("babyai-backend");

if backend_binary.exists() {
    // Production mode: use bundled backend
    Command::new(&backend_binary)...
} else if cfg!(debug_assertions) {
    // Development mode: use system Python
    Command::new("python3.14")...
}
```

**Validation:**
```bash
# Build the bundled backend first
cd baby-ai-python
pyinstaller baby-ai-backend.spec

# Start Tauri in dev mode (should detect and use bundled backend)
cd baby-ai-desktop
npm run tauri dev

# Check logs - should see: "Launching bundled backend: ..."
```

#### Step 9.5.6: Add Tauri v2 Capabilities for Process Spawning

**File:** `src-tauri/capabilities/default.json`

**Content:**
```json
{
  "$schema": "https://tauri.app/schema/capabilities.json",
  "identifier": "default",
  "description": "Default capabilities for Baby AI",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "shell:allow-execute",
    "shell:allow-spawn"
  ]
}
```

**Why:** Tauri v2 uses a capabilities model. We need `shell:allow-execute` and `shell:allow-spawn` to launch the Python backend and Ollama processes.

**Update:** `src-tauri/tauri.conf.json`

Add capabilities reference:
```json
{
  "app": {
    "security": {
      "capabilities": ["default"]
    }
  }
}
```

#### Step 9.5.7: Download and Bundle Ollama Server v0.12.10

**Goal:** Include Ollama Server v0.12.10 binary in the Tauri app bundle so users don't need to install Ollama separately.

**Download Ollama Server v0.12.10:**
```bash
# Create directory for bundled binaries
mkdir -p baby-ai-desktop/src-tauri/binaries

# Download Ollama Server v0.12.10 for macOS
cd baby-ai-desktop/src-tauri/binaries

# For Apple Silicon (arm64)
wget https://github.com/ollama/ollama/releases/download/v0.12.10/ollama-darwin-arm64
chmod +x ollama-darwin-arm64

# For Intel (x86_64) - optional, if supporting both architectures
wget https://github.com/ollama/ollama/releases/download/v0.12.10/ollama-darwin-amd64
chmod +x ollama-darwin-amd64
```

**Update Tauri Config to Include Ollama Binary:**

**File:** `src-tauri/tauri.conf.json`

Add to bundle resources:
```json
{
  "bundle": {
    "resources": [
      "../binaries/ollama-darwin-*"
    ]
  }
}
```

**Note:** The `BackendManager::start_ollama()` function in **Phase 9.2** (Step 9.2) already implements the unified logic with fallback:

1. **First attempt:** Try to start system Ollama (via `try_start_system_ollama()`)
2. **Fallback:** If system Ollama fails, try bundled Ollama Server v0.12.10 (via `try_start_bundled_ollama()`)
3. **Helper function:** `get_bundled_ollama_path()` detects architecture (arm64/amd64) and locates the bundled binary

The unified function handles both development (system Ollama) and production (bundled binary) scenarios automatically.

**Validation:**
```bash
# Build Tauri app with bundled Ollama
cd baby-ai-desktop
npm run tauri build

# Test the bundled app
# The app should automatically start Ollama Server v0.12.10 if not already running
```

#### Step 9.5.8: macOS Codesigning (Production)

**Note:** For production DMG distribution, both the bundled backend AND Ollama Server v0.12.10 binary must be codesigned.

**Commands (when ready for production):**
```bash
# Sign the backend executable
codesign --force --sign "Developer ID Application: Your Name" \
  dist/babyai-backend/babyai-backend

# Sign the Ollama Server v0.12.10 binary
codesign --force --sign "Developer ID Application: Your Name" \
  baby-ai-desktop/src-tauri/binaries/ollama-darwin-arm64

# Verify signatures
codesign --verify --verbose dist/babyai-backend/babyai-backend
codesign --verify --verbose baby-ai-desktop/src-tauri/binaries/ollama-darwin-arm64
```

**For Phase 1.1 (dev/testing):** Skip codesigning. It's only required for distribution.

#### Step 9.5.8: Test Bundled Backend in Tauri

**Commands:**
```bash
# Ensure bundled backend exists
cd baby-ai-python
ls dist/babyai-backend/babyai-backend

# Start Tauri (should auto-launch bundled backend)
cd baby-ai-desktop
npm run tauri dev
```

**Validation:**
- [ ] Tauri window opens
- [ ] Console shows "Launching bundled backend: ..."
- [ ] Backend health check passes
- [ ] Can send chat messages and get responses
- [ ] No "python3.14 not found" errors

**Acceptance Criteria:**
- [ ] Bundled backend executable created successfully
- [ ] Backend runs standalone without Python installation
- [ ] Tauri detects and launches bundled backend in production mode
- [ ] Falls back to system Python only in debug mode
- [ ] All API endpoints work with bundled backend
- [ ] No import errors or missing dependencies

---

### Phase 10: Minimal Chat UI with React + TypeScript (3 hours)

**Note:** This phase creates a minimal ChatPage using React + TypeScript + Tailwind CSS (same stack as the old Baby AI frontend) but with simplified scope - only the chat interface for testing, no other pages.

#### Step 10.1: Initialize Tauri + React Frontend

**Commands:**
```bash
# Ensure Node 25 is active
nvm use 25
node -v  # Should show v25.1.0
npm -v   # Should show 11.6.2

# Install Tauri CLI v2 (if not already installed)
cargo install tauri-cli --version ^2.0

# Create Tauri v2 app with React template
cd baby-ai-python
npm create tauri-app@latest
# Choose: React + TypeScript
# App name: baby-ai-desktop
# Window title: Baby AI
# Use Tauri v2

cd baby-ai-desktop
```

**Note:** This creates a Tauri v2.9.x app with React 19.2.0, TypeScript 5.9.3, and Vite 7.2.2.

#### Step 10.2: Install Frontend Dependencies

**Commands:**
```bash
# Ensure Node 25 is active
nvm use 25

# Install all dependencies (versions verified compatible with Node 25.1.0)
npm install react@19.2.0 react-dom@19.2.0 @tauri-apps/api@2.9.0 zustand@5.0.8 sonner@2.0.7 lucide-react@0.553.0 react-router-dom@7.9.5

# Install dev dependencies
npm install -D @types/react@19.2.2 @types/react-dom@19.2.2 @vitejs/plugin-react@5.1.0 @tauri-apps/cli@2.9.4 typescript@5.9.3 vite@7.2.2 tailwindcss@4.1.17 autoprefixer@10.4.22 postcss@8.5.6 clsx@2.1.1 class-variance-authority@0.7.1 tailwind-merge@3.4.0 tailwindcss-animate@1.0.7

# Initialize Tailwind (if needed)
npx tailwindcss init -p
```

**Update `tailwind.config.js`:**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Update `src/index.css`:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### Step 10.3: Create Minimal ChatPage Component (`src/components/ChatPage.tsx`)

**Content:**
```typescript
import { useState, useEffect, useRef } from 'react';

const API_BASE_URL = 'http://127.0.0.1:8000';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'error';
  content: string;
}

export function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    checkBackendStatus();
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      setIsConnected(data.status === 'healthy');
    } catch (error) {
      setIsConnected(false);
    }
  };

  const sendMessage = async (useStreaming = false) => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      if (useStreaming) {
        // Streaming mode with NDJSON reader
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userMessage.content,
            conversation_id: conversationId,
            stream: true,
          }),
        });

        if (!response.body) throw new Error('No response body');

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let assistantContent = '';
        const assistantId = (Date.now() + 1).toString();

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (!line.trim()) continue;

            try {
              const chunk = JSON.parse(line);

              if (chunk.type === 'meta') {
                setConversationId(chunk.conversation_id);
              } else if (chunk.type === 'delta') {
                assistantContent += chunk.content;
                setMessages((prev) => {
                  const existing = prev.find((m) => m.id === assistantId);
                  if (existing) {
                    return prev.map((m) =>
                      m.id === assistantId ? { ...m, content: assistantContent } : m
                    );
                  } else {
                    return [
                      ...prev,
                      { id: assistantId, role: 'assistant', content: assistantContent },
                    ];
                  }
                });
              }
            } catch (e) {
              console.error('Failed to parse chunk:', line, e);
            }
          }
        }
      } else {
        // Non-streaming mode (default)
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: userMessage.content,
            conversation_id: conversationId,
            stream: false,
          }),
        });

        const data = await response.json();
        setConversationId(data.conversation_id);

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.message,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'error',
        content: 'Sorry, I encountered an error. Please make sure the backend is running.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-purple-600 to-purple-800">
      <header className="bg-white/10 backdrop-blur-sm text-white p-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">🤖 Baby AI</h1>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
          <span className="text-sm">{isConnected ? 'Connected' : 'Offline'}</span>
        </div>
      </header>

      <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-white/80 mt-20">
            <h2 className="text-3xl font-bold mb-4">Welcome to Baby AI!</h2>
            <p className="mb-6">I can help you control macOS applications. Try commands like:</p>
            <div className="space-y-2 max-w-md mx-auto">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">"Open Safari"</div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">"Close TextEdit"</div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3">"Launch Spotify"</div>
            </div>
          </div>
        ) : (
          messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-purple-500 to-purple-700 text-white'
                    : msg.role === 'error'
                    ? 'bg-red-100 text-red-800'
                    : 'bg-white text-gray-800'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="p-4 bg-white/10 backdrop-blur-sm">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a command..."
            disabled={isLoading}
            className="flex-1 px-4 py-3 rounded-full bg-white text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-400"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-white text-purple-600 rounded-full font-semibold hover:bg-purple-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

#### Step 10.4: Update App.tsx

**Content:**
```typescript
import { ChatPage } from './components/ChatPage';

function App() {
  return <ChatPage />;
}

export default App;
```

#### Step 10.5: Configure Tauri Backend Manager (`src-tauri/src/main.rs`)

**Content:**
```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::{Command, Child};
use std::sync::Mutex;
use tauri::State;

struct BackendProcess(Mutex<Option<Child>>);

#[tauri::command]
fn start_backend(backend: State<BackendProcess>) -> Result<String, String> {
    let mut process = backend.0.lock().unwrap();
    
    if process.is_some() {
        return Ok("Backend already running".to_string());
    }
    
    // Start Python backend
    let child = Command::new("python3")
        .arg("-m")
        .arg("uvicorn")
        .arg("src.main:app")
        .arg("--host")
        .arg("127.0.0.1")
        .arg("--port")
        .arg("8000")
        .spawn()
        .map_err(|e| format!("Failed to start backend: {}", e))?;
    
    *process = Some(child);
    Ok("Backend started successfully".to_string())
}

fn main() {
    tauri::Builder::default()
        .manage(BackendProcess(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![start_backend])
        .setup(|app| {
            // Auto-start backend on app launch
            let backend = app.state::<BackendProcess>();
            let _ = start_backend(backend);
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

#### Step 10.6: Test UI

**Commands:**
```bash
# Ensure backend dependencies are installed
cd baby-ai-python
source venv/bin/activate
pip install -r requirements.txt

# Start Tauri in dev mode (will auto-start Python backend)
cd baby-ai-desktop
npm run tauri dev
```

**Validation:**
- [ ] Tauri window opens with modern chat UI
- [ ] Status shows "Connected" (green dot)
- [ ] Can type message and press Enter or click Send
- [ ] User message appears on right (purple gradient bubble)
- [ ] Assistant response appears on left (white bubble)
- [ ] Test "Open TextEdit" - should work
- [ ] Test "Open FakeApp123" - should show friendly error in red bubble
- [ ] UI is responsive and matches Tailwind styling

---

## Acceptance Criteria Validation

Before marking Phase 1.1 complete, verify ALL criteria:

### Functional Requirements
- [ ] App not installed scenario returns friendly error (no crash)
- [ ] Valid function calling (LLM generates valid JSON that passes Pydantic validation)
- [ ] Validation retry works (up to 3 attempts with backoff)
- [ ] Tool whitelist enforced (only open_app and close_app callable)
- [ ] Natural language UX (all responses friendly and conversational)
- [ ] Logging complete (agent_name, domain, step_id, result in all logs)
- [ ] Conversation tracking (conversation_id persists across turns, step_id unique per turn)
- [ ] Streaming support (/api/chat with stream=true returns NDJSON chunks)
- [ ] Non-streaming support (/api/chat with stream=false returns complete JSON)
- [ ] Tauri launches Python backend automatically
- [ ] Tauri launches Ollama automatically (or detects if already running)
- [ ] Frontend can communicate with backend via HTTP
- [ ] Chat UI displays messages correctly (user right, assistant left)

### Performance Requirements
- [ ] End-to-end latency < 3 seconds (p95) on warm LLM
- [ ] Tool execution < 500ms for app open/close
- [ ] No memory leaks (run for 1 hour, monitor memory)

### Testing Requirements
- [ ] Unit tests: 90%+ coverage
- [ ] Integration tests: Happy path and error scenarios pass
- [ ] Manual testing: Verified on macOS with Qwen3-4B-Thinking-2507-Q8_0

### Documentation Requirements
- [ ] API documentation (OpenAPI/Swagger auto-generated by FastAPI)
- [ ] README with setup instructions
- [ ] Architecture diagram in design doc

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 0 | Environment Setup | 30m | 30m |
| 1 | Core Data Models | 1h | 1h 30m |
| 2 | LLM Client Layer | 2h | 3h 30m |
| 3 | App Agent | 2h | 5h 30m |
| 4 | Orchestrator | 3h | 8h 30m |
| 5 | FastAPI Backend | 2h | 10h 30m |
| 6 | Testing | 3h | 13h 30m |
| 7 | Manual Validation | 1h | 14h 30m |
| 8 | Documentation | 1h | 15h 30m |
| 9 | Tauri Integration | 3h | 18h 30m |
| 9.5 | Python Backend Bundling | 2h | 20h 30m |
| 10 | Minimal Chat UI (React + TS) | 3h | 23h 30m |

**Total Estimated Time:** 23.5 hours (~3 days)

---

## Next Steps After Phase 1.1

1. **Phase 2.0**: Add Browser Agent
2. **Phase 3.0**: Add Window Agent
3. **Phase 4.0**: Implement Router Agent for multi-agent orchestration
4. **Phase 5.0**: Add Safety Agent and escalation (like old Baby AI Fallback.md)
5. **Future**: Add warm-up for Ollama model (optimization)

---

**Document Status:** Ready for Execution  
**Approval Required:** Yes  
**Next Action:** Get user approval and begin Phase 0
