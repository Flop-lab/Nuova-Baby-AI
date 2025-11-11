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
    llm_client: LLMClient,
    config: OrchestratorConfig,
    conversation_id: Optional[str] = None
) -> ChatResponse:
    """
    Orchestrate the LLM call and tool execution with retry logic.
    """
    retries = 0
    max_retries = config.max_validation_retries
    trace = None
    reply = ""
    while retries <= max_retries:
        try:
            # Simulazione chiamata LLM e tool
            tool_call = ToolCall(function=None)
            agent = AppAgent()
            result = agent.execute(tool_call)
            trace = AgentTrace(tool_call=tool_call, result=result)
            reply = result.output or result.error or "No output"
            break
        except ValidationError as ve:
            logger.warning("Validation error", error=str(ve))
            retries += 1
            reply = f"Validation error: {ve} (retry {retries}/{max_retries})"
        except Exception as e:
            logger.error("Orchestration error", error=str(e))
            reply = f"Error: {e}"
            break
    return ChatResponse(reply=reply, trace=trace)
