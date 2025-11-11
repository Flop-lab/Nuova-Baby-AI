import ollama
from typing import List, Dict, Any, Optional
from src.llm.client import LLMClient
import structlog

logger = structlog.get_logger()

class OllamaAdapter(LLMClient):
    """Ollama implementation of LLM client"""
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        # Esempio di chiamata a Ollama
        response = ollama.generate(model=kwargs.get('model', 'mistral:7b-instruct'), prompt=prompt)
        logger.info("Ollama response", response=response)
        return response
