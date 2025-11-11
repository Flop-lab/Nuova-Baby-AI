from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator
import structlog
import json
import uuid

from src.models.config import OrchestratorConfig
from src.models.schemas import ChatRequest, ChatResponse, ChatChunk
from src.llm.ollama_adapter import OllamaAdapter
from src.llm.client import LLMClient
from src.orchestrator.orchestrator import orchestrate_with_retry
from src.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Global instances
llm_client: Optional[LLMClient] = OllamaAdapter(model="qwen3:4b-thinking-2507-q8_0")
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

async def stream_chat_response(user_message: str) -> AsyncGenerator[str, None]:
    """
    Generate NDJSON streaming chunks for chat response.

    Yields:
        - Meta chunk with conversation_id and step_id
        - Delta chunks with partial content (character by character)
        - Final chunk with complete message
    """
    conversation_id = str(uuid.uuid4())
    step_id = str(uuid.uuid4())

    # Meta chunk
    meta_chunk = ChatChunk(
        type="meta",
        conversation_id=conversation_id,
        step_id=step_id
    )
    yield json.dumps(meta_chunk.model_dump(exclude_none=True)) + "\n"

    # Get full response from orchestrator
    response = await orchestrate_with_retry(
        user_message=user_message,
        llm_client=llm_client,
        config=orchestrator_config,
        conversation_id=conversation_id
    )

    # Delta chunks (stream character by character)
    for char in response.reply:
        delta_chunk = ChatChunk(
            type="delta",
            content=char
        )
        yield json.dumps(delta_chunk.model_dump(exclude_none=True)) + "\n"

    # Final chunk
    final_chunk = ChatChunk(
        type="final",
        message=response.reply
    )
    yield json.dumps(final_chunk.model_dump(exclude_none=True)) + "\n"


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
    """Main chat endpoint with streaming support"""
    try:
        # Validate LLM client is initialized
        if llm_client is None:
            logger.error("llm_client_not_initialized")
            raise HTTPException(
                status_code=500,
                detail="LLM client not initialized"
            )

        logger.info("chat_request_received", message_length=len(request.message), stream=request.stream)

        # Streaming mode
        if request.stream:
            return StreamingResponse(
                stream_chat_response(request.message),
                media_type="application/x-ndjson"
            )

        # Non-streaming mode
        response = await orchestrate_with_retry(
            user_message=request.message,
            llm_client=llm_client,
            config=orchestrator_config,
            conversation_id=None
        )

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
