from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator
import structlog
import json
import uuid
import logfire  # Pydantic Logfire for observability

from src.models.schemas import ChatRequest, ChatResponse, ChatChunk
from src.agents.pydantic_agent import run_agent_non_streaming, run_agent_streaming
from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

app = FastAPI(title="Baby AI Backend", version="1.1.0")

# Note: FastAPI instrumentation requires: pip install 'logfire[fastapi]'
# For now, Pydantic AI is automatically instrumented

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
        "pydantic_ai_enabled": True,
        "version": "1.1.0"
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint with streaming support using Pydantic AI"""
    try:
        logger.info("chat_request_received", message_length=len(request.message), stream=request.stream)

        # Streaming mode - use Pydantic AI streaming
        if request.stream:
            return StreamingResponse(
                run_agent_streaming(request.message),
                media_type="application/x-ndjson"
            )

        # Non-streaming mode - use Pydantic AI
        response = await run_agent_non_streaming(request.message)

        logger.info("chat_response_sent", reply_length=len(response.reply))
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error("chat_endpoint_error", error=str(e), error_type=type(e).__name__)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
