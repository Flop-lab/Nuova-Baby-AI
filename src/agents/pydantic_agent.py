"""
Pydantic AI Agent for Baby AI
Replaces custom orchestrator with production-grade Pydantic AI framework

Official Docs: https://ai.pydantic.dev
"""

import os
import uuid
import json
from typing import Optional
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from appscript import app as appscript_app
import structlog
import logfire  # REQUIRED for debugging and observability

from src.models.schemas import ChatResponse, ChatChunk
from src.orchestrator.prompts import SYSTEM_PROMPT

logger = structlog.get_logger()

# ============================================================================
# Configure Logfire (REQUIRED - BEFORE creating agent)
# ============================================================================

logfire.configure(
    service_name='baby-ai-backend',
    service_version='1.1.0',
    send_to_logfire='if-token-present',  # Uses local auth in dev, LOGFIRE_TOKEN in prod
)

# Instrument Pydantic AI for automatic tracing
logfire.instrument_pydantic_ai()

# ============================================================================
# Create Pydantic AI Agent with Ollama Model
# ============================================================================
# Using OpenAIChatModel with OllamaProvider for Ollama compatibility
# Ollama uses OpenAI-compatible API at /v1 endpoint

ollama_model = OpenAIChatModel(
    model_name='qwen3:4b-thinking-2507-q4_K_M',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),
)

agent = Agent(
    ollama_model,
    instructions=SYSTEM_PROMPT,  # Use 'instructions' for single-turn (no history)
    retries=3,  # Automatic retry on failures
)

# ============================================================================
# Register Tools with @agent.tool Decorator
# ============================================================================
# Tools use RunContext as first parameter for dependency injection
# Docstrings are extracted by Pydantic AI and sent to LLM as tool descriptions

@agent.tool
def open_app(ctx: RunContext, appName: str) -> str:
    """
    Open a macOS application by name.

    Args:
        appName: The name of the application to open (e.g., "Safari", "Spotify", "Chrome")

    Returns:
        Success message or error description
    """
    try:
        appscript_app(appName).activate()
        logger.info("open_app_success", app_name=appName)
        logfire.info("App opened successfully", app_name=appName)  # Logfire tracing
        return f"I've opened {appName} successfully."
    except Exception as e:
        logger.error("open_app_failed", app_name=appName, error=str(e))
        logfire.error("Failed to open app", app_name=appName, error=str(e))  # Logfire error tracking
        return f"Failed to open {appName}: {str(e)}"


@agent.tool
def close_app(ctx: RunContext, appName: str) -> str:
    """
    Close a macOS application by name.

    Args:
        appName: The name of the application to close (e.g., "Safari", "Spotify", "Chrome")

    Returns:
        Success message or error description
    """
    try:
        appscript_app(appName).quit()
        logger.info("close_app_success", app_name=appName)
        logfire.info("App closed successfully", app_name=appName)  # Logfire tracing
        return f"I've closed {appName} successfully."
    except Exception as e:
        logger.error("close_app_failed", app_name=appName, error=str(e))
        logfire.error("Failed to close app", app_name=appName, error=str(e))  # Logfire error tracking
        return f"Failed to close {appName}: {str(e)}"


# ============================================================================
# Non-Streaming Runner
# ============================================================================

async def run_agent_non_streaming(user_message: str) -> ChatResponse:
    """
    Run Pydantic AI agent and return ChatResponse.

    Args:
        user_message: User's natural language request

    Returns:
        ChatResponse with agent's reply
    """
    conversation_id = str(uuid.uuid4())
    step_id = str(uuid.uuid4())

    logger.info(
        "pydantic_agent_start_non_streaming",
        user_message=user_message,
        conversation_id=conversation_id,
    )

    try:
        # Run agent with automatic tool calling and retry
        result = await agent.run(user_message)

        # Access output via .output (not .data)
        # For Agent[None, str], result.output is a string
        reply = result.output

        logger.info(
            "pydantic_agent_complete",
            conversation_id=conversation_id,
            step_id=step_id,
            reply_length=len(reply),
            messages_count=len(result.all_messages())  # Access message history
        )

        return ChatResponse(
            reply=reply,
            conversation_id=conversation_id,
            step_id=step_id,
            trace=None,
        )

    except Exception as e:
        logger.error(
            "pydantic_agent_error",
            error=str(e),
            error_type=type(e).__name__,
            conversation_id=conversation_id,
        )
        return ChatResponse(
            reply=f"I encountered an error: {str(e)}",
            conversation_id=conversation_id,
            step_id=step_id,
            trace=None,
        )


# ============================================================================
# Streaming Runner
# ============================================================================

async def run_agent_streaming(user_message: str):
    """
    Run Pydantic AI agent with streaming response.

    Yields ChatChunk objects compatible with existing API:
    - meta chunk (conversation_id, step_id)
    - delta chunks (partial content)
    - final chunk (complete message)

    Uses Pydantic AI's stream_text() method with delta=True for incremental chunks.
    Docs: https://ai.pydantic.dev/api/result/#pydantic_ai.result.StreamedRunResult.stream_text

    Args:
        user_message: User's natural language request

    Yields:
        JSON-encoded ChatChunk strings (NDJSON format)
    """
    conversation_id = str(uuid.uuid4())
    step_id = str(uuid.uuid4())

    # Yield meta chunk first
    meta_chunk = ChatChunk(
        type="meta",
        conversation_id=conversation_id,
        step_id=step_id
    )
    yield json.dumps(meta_chunk.model_dump(exclude_none=True)) + "\n"

    logger.info(
        "pydantic_agent_start_streaming",
        user_message=user_message,
        conversation_id=conversation_id,
    )

    try:
        # Use Pydantic AI's streaming API
        accumulated_text = ""

        # run_stream() returns StreamedRunResult context manager
        async with agent.run_stream(user_message) as result:
            # stream_text(delta=True) yields incremental text chunks
            # delta=True means each chunk is only new text (not cumulative)
            async for text_chunk in result.stream_text(delta=True):
                accumulated_text += text_chunk

                # Yield delta chunk (Pydantic AI already chunks appropriately)
                delta_chunk = ChatChunk(
                    type="delta",
                    content=text_chunk  # Already a string chunk from Pydantic AI
                )
                yield json.dumps(delta_chunk.model_dump(exclude_none=True)) + "\n"

        # Yield final chunk with complete message
        final_chunk = ChatChunk(
            type="final",
            message=accumulated_text
        )
        yield json.dumps(final_chunk.model_dump(exclude_none=True)) + "\n"

        logger.info(
            "pydantic_agent_streaming_complete",
            conversation_id=conversation_id,
            step_id=step_id,
            message_length=len(accumulated_text)
        )

    except Exception as e:
        logger.error(
            "pydantic_agent_streaming_error",
            error=str(e),
            error_type=type(e).__name__,
            conversation_id=conversation_id,
        )
        # Yield error as final chunk
        error_chunk = ChatChunk(
            type="final",
            message=f"I encountered an error: {str(e)}"
        )
        yield json.dumps(error_chunk.model_dump(exclude_none=True)) + "\n"
