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
    try:
        # Validate LLM client is initialized
        if llm_client is None:
            logger.error("llm_client_not_initialized")
            raise HTTPException(
                status_code=500,
                detail="LLM client not initialized"
            )

        logger.info("chat_request_received", message_length=len(request.message))

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
