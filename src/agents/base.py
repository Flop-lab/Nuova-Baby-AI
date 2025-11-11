from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.models.schemas import ToolCall, ExecutionResult

class BaseAgent(ABC):
    """Base class for all domain agents"""
    @abstractmethod
    def get_tools(cls) -> List[Dict[str, Any]]:
        """Return tool definitions for the agent."""
        pass

    @abstractmethod
    def execute(self, tool_call: ToolCall) -> ExecutionResult:
        """Execute a tool call and return the result."""
        pass
