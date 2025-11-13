import asyncio
import uuid
from typing import Optional, List, Dict, Any
from pydantic import ValidationError
from src.llm.ollama_adapter import OllamaAdapter
from src.agents.app_agent import AppAgent
from src.agents.browser_agent import BrowserAgent
from src.models.schemas import ChatRequest, ChatResponse, ToolCall, AgentTrace
from src.models.config import OrchestratorConfig
from src.orchestrator.prompts import SYSTEM_PROMPT
import structlog

logger = structlog.get_logger()


async def orchestrate_with_retry(
    user_message: str,
    llm_client: OllamaAdapter,
    config: OrchestratorConfig,
    conversation_id: Optional[str] = None
) -> ChatResponse:
    """
    Orchestrate LLM call with tool execution loop and retry logic.

    Flow:
    1. Send user message with system prompt and available tools
    2. LLM decides whether to call tools (with think=True for reasoning)
    3. If tool calls: execute them and send results back to LLM
    4. Get final natural language response
    5. Retry on validation errors

    Args:
        user_message: User's natural language request
        llm_client: OllamaAdapter instance
        config: Orchestrator configuration
        conversation_id: Optional conversation ID for tracking

    Returns:
        ChatResponse with final reply and execution trace
    """
    retries = 0
    max_retries = config.max_validation_retries
    conversation_id = conversation_id or str(uuid.uuid4())

    logger.info(
        "orchestrator_start",
        user_message=user_message,
        conversation_id=conversation_id,
        model=llm_client.model
    )

    # Get tools from all agents
    tool_functions = []
    tool_functions.extend(AppAgent.get_tool_functions())
    tool_functions.extend(BrowserAgent.get_tool_functions())

    available_functions = {}
    available_functions.update(AppAgent.get_available_functions())
    available_functions.update(BrowserAgent.get_available_functions())

    # Initialize message history
    messages: List[Dict[str, Any]] = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': user_message}
    ]

    while retries <= max_retries:
        try:
            # Agentic loop: continue calling LLM until it stops requesting tool calls
            max_iterations = 10  # Prevent infinite loops
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # Step 1: Call LLM with tools and think=True
                logger.info("llm_call", iteration=iteration, num_messages=len(messages))

                response = llm_client.chat(
                    messages=messages,
                    tools=tool_functions,
                    think=True  # Enable extended thinking/reasoning
                )

                # Log thinking process if available
                if hasattr(response.message, 'thinking') and response.message.thinking:
                    logger.info("llm_thinking", thinking=response.message.thinking[:200])

                # Step 2: Check if LLM wants to call tools
                if hasattr(response.message, 'tool_calls') and response.message.tool_calls:
                    logger.info("tool_calls_detected", num_calls=len(response.message.tool_calls))

                    # Append assistant message with tool calls to history
                    messages.append(response.message)

                    # Step 3: Execute each tool call
                    for tool_call in response.message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = tool_call.function.arguments

                        logger.info(
                            "executing_tool",
                            function=function_name,
                            arguments=function_args
                        )

                        # Get the function and execute it
                        if function_to_call := available_functions.get(function_name):
                            try:
                                # Execute the tool function
                                tool_result = function_to_call(**function_args)
                                logger.info(
                                    "tool_executed",
                                    function=function_name,
                                    result_preview=str(tool_result)[:100]
                                )

                                # Append tool result to messages
                                messages.append({
                                    'role': 'tool',
                                    'content': str(tool_result),
                                    'tool_name': function_name
                                })

                            except Exception as tool_error:
                                error_msg = f"Error executing {function_name}: {str(tool_error)}"
                                logger.error("tool_execution_error", function=function_name, error=str(tool_error))

                                # Append error as tool result
                                messages.append({
                                    'role': 'tool',
                                    'content': error_msg,
                                    'tool_name': function_name
                                })
                        else:
                            logger.error("unknown_function", function=function_name)
                            messages.append({
                                'role': 'tool',
                                'content': f"Unknown function: {function_name}",
                                'tool_name': function_name
                            })

                    # Continue the loop - LLM will decide next action (more tools or final response)
                    continue

                else:
                    # No tool calls - LLM provided final response
                    reply = response.message.content or "I completed the task."
                    step_id = str(uuid.uuid4())

                    logger.info(
                        "orchestration_complete",
                        conversation_id=conversation_id,
                        step_id=step_id,
                        reply_length=len(reply),
                        total_iterations=iteration
                    )

                    return ChatResponse(
                        reply=reply,
                        conversation_id=conversation_id,
                        step_id=step_id,
                        trace=None
                    )

            # Max iterations reached
            step_id = str(uuid.uuid4())
            logger.warning("max_iterations_reached", max_iterations=max_iterations, step_id=step_id)
            return ChatResponse(
                reply="I completed the requested actions.",
                conversation_id=conversation_id,
                step_id=step_id,
                trace=None
            )

        except ValidationError as ve:
            retries += 1
            logger.warning(
                "validation_error",
                error=str(ve),
                attempt=retries,
                max_retries=max_retries
            )

            if retries > max_retries:
                step_id = str(uuid.uuid4())
                error_reply = f"I encountered a validation error after {max_retries} attempts. Please try rephrasing your request."
                return ChatResponse(
                    reply=error_reply,
                    conversation_id=conversation_id,
                    step_id=step_id,
                    trace=None
                )

            # Continue to next retry
            continue

        except Exception as e:
            step_id = str(uuid.uuid4())
            logger.error(
                "orchestration_error",
                error=str(e),
                error_type=type(e).__name__,
                conversation_id=conversation_id,
                step_id=step_id
            )
            error_reply = f"I encountered an unexpected error: {str(e)}"
            return ChatResponse(
                reply=error_reply,
                conversation_id=conversation_id,
                step_id=step_id,
                trace=None
            )

    # Should not reach here, but just in case
    step_id = str(uuid.uuid4())
    return ChatResponse(
        reply="Maximum retries exceeded. Please try again.",
        conversation_id=conversation_id,
        step_id=step_id,
        trace=None
    )
