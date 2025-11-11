import ollama
from typing import List, Dict, Any, Optional, Callable
from src.llm.client import LLMClient
import structlog

logger = structlog.get_logger()


class OllamaAdapter(LLMClient):
    """Ollama implementation of LLM client with tool calling support"""

    def __init__(self, model: str = "qwen2.5:7b-instruct", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama adapter.

        Args:
            model: Model name (default: qwen2.5:7b-instruct)
            base_url: Ollama server URL
        """
        self.model = model
        self.base_url = base_url
        logger.info("OllamaAdapter initialized", model=model, base_url=base_url)

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Legacy generate method"""
        model = kwargs.get('model', self.model)
        response = ollama.generate(model=model, prompt=prompt)
        logger.info("Ollama generate", model=model, prompt_length=len(prompt))
        return response

    def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Callable]] = None,
        think: bool = True,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat with Ollama with optional tool calling support.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of Python functions to use as tools
            think: Enable extended thinking/reasoning (default: True)
            stream: Enable streaming response (default: False)
            **kwargs: Additional parameters for ollama.chat()

        Returns:
            Response dict with message and optional tool_calls
        """
        model = kwargs.get('model', self.model)

        chat_params = {
            'model': model,
            'messages': messages,
        }

        # Add tools if provided
        if tools:
            chat_params['tools'] = tools
            logger.info("chat_with_tools", model=model, num_tools=len(tools), think=think)

        # Add think parameter if tools are present
        if tools and think:
            chat_params['think'] = True

        # Add stream parameter
        if stream:
            chat_params['stream'] = stream

        try:
            response = ollama.chat(**chat_params)

            # Log response details
            if hasattr(response, 'message'):
                has_tool_calls = hasattr(response.message, 'tool_calls') and response.message.tool_calls
                logger.info(
                    "ollama_chat_response",
                    model=model,
                    has_tool_calls=has_tool_calls,
                    has_content=bool(getattr(response.message, 'content', None)),
                    has_thinking=hasattr(response.message, 'thinking') and bool(response.message.thinking)
                )

            return response

        except Exception as e:
            logger.error("ollama_chat_error", model=model, error=str(e), error_type=type(e).__name__)
            raise
