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

### Phase 7: Manual Testing & Validation (1 hour) ✅ COMPLETED

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

### Phase 8: Documentation (1 hour) ✅ COMPLETED

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

**Document Status:** Ready for Execution  
**Approval Required:** Yes  
**Next Action:** Get user approval and begin Phase 9
