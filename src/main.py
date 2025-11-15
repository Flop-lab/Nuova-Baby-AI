from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Optional
import structlog

from src.models.schemas import ChatRequest, ChatResponse
from src.agents.pydantic_agent import (
    run_agent_non_streaming,
    run_agent_streaming,
)
from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

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
        "llm_initialized": True,  # Pydantic AI handles initialization
        "version": "1.1.0",
        "agent": "pydantic-ai"  # New field to indicate Pydantic AI is active
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint with Pydantic AI integration"""
    try:
        logger.info(
            "chat_request_received",
            message_length=len(request.message),
            stream=request.stream
        )

        # Streaming mode
        if request.stream:
            return StreamingResponse(
                run_agent_streaming(request.message),
                media_type="application/x-ndjson"
            )

        # Non-streaming mode
        response = await run_agent_non_streaming(request.message)

        logger.info("chat_response_sent", reply_length=len(response.reply))
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "chat_endpoint_error",
            error=str(e),
            error_type=type(e).__name__
        )
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
