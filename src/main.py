from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from typing import Optional
import structlog

from src.models.config import OrchestratorConfig
from src.models.schemas import ChatRequest, ChatResponse
from src.llm.ollama_adapter import OllamaAdapter
from src.llm.client import LLMClient
from src.orchestrator.orchestrator import orchestrate_with_retry

# Setup logging
logger = structlog.get_logger()

# Global instances
llm_client: Optional[LLMClient] = OllamaAdapter()
orchestrator_config = OrchestratorConfig()

app = FastAPI(title="Baby AI Backend", version="1.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_initialized": llm_client is not None,
        "version": "1.1.0"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    response = await orchestrate_with_retry(
        user_message=request.message,
        llm_client=llm_client,
        config=orchestrator_config,
        conversation_id=None
    )
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
