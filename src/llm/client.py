from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class LLMClient(ABC):
    """Abstract interface for LLM providers"""
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the LLM."""
        pass
