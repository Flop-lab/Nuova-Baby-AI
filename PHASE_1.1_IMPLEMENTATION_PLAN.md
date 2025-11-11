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
**Prerequisites:** macOS with Python 3.14, Ollama Server v0.12.10 installed, Mistral 7B model pulled, Node.js 25 (via nvm), Rust 1.91.1 for Tauri

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

### Phase 0: Environment Setup (30 minutes)

#### Step 0.1: Create Project Directory
```bash
# Esempio per macOS:
cd ~/Developer
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
# Se hai già il file requirements.txt nella cartella del progetto:
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
ollama list | grep mistral
```

**Expected:** Mistral 7B Instruct model present

**If missing:**
```bash
ollama pull mistral:7b-instruct
ollama pull nomic-embed-text
```

---

### Phase 1: Core Data Models (1 hour)

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

### Phase 2: LLM Client Layer (2 hours)

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

### Phase 3: App Agent Implementation (2 hours)

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

### Phase 4: Orchestrator Logic (3 hours)

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

### Phase 5: FastAPI Backend (2 hours)

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
LLM_MODEL=mistral:7b-instruct
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

### Phase 6: Testing (3 hours)

#### Step 6.1: Unit Tests for App Agent (`tests/test_app_agent.py`)

**Content:**
```python
import pytest
from src.agents.app_agent import AppAgent
from src.models.schemas import ToolCall, FunctionCall

@pytest.mark.asyncio
async def test_app_agent_tools():
    """Test that AppAgent returns correct tool definitions"""
    /* Lines 1159-1168 omitted */
    assert open_params["required"] == ["appName"]

@pytest.mark.asyncio
