from pydantic import BaseModel, Field
from typing import Literal, Optional, Dict, Any, List
from datetime import datetime

class FunctionCall(BaseModel):
    """Function name and arguments"""
    name: str = Field(description="Function name")
    arguments: Dict[str, Any] = Field(description="Function arguments as dict")

class ToolCall(BaseModel):
    """Represents a function call from the LLM"""
    id: Optional[str] = Field(default=None, description="Unique call ID")
    function: FunctionCall

class ExecutionResult(BaseModel):
    """Result of tool execution"""
    success: bool = Field(description="Execution success status")
    output: Optional[Any] = Field(default=None, description="Output of the tool")
    error: Optional[str] = Field(default=None, description="Error message if any")
    duration_ms: float = Field(description="Execution time in milliseconds")

class AgentTrace(BaseModel):
    """Telemetry and logging data"""
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Trace timestamp")
    tool_call: Optional[ToolCall] = Field(default=None, description="Tool call details")
    result: Optional[ExecutionResult] = Field(default=None, description="Result of execution")
    confidence: Optional[float] = Field(default=None, description="LLM confidence score")

class ChatRequest(BaseModel):
    """User request to the API"""
    message: str = Field(description="User message")
    stream: bool = Field(default=False, description="Enable streaming response")

class ChatResponse(BaseModel):
    """Response from the API"""
    reply: str = Field(description="LLM or agent reply")
    trace: Optional[AgentTrace] = Field(default=None, description="Execution trace")

class ChatChunk(BaseModel):
    """Streaming response chunk"""
    chunk: str = Field(description="Partial response chunk")
    usage: Optional[Dict[str, int]] = Field(default=None, description="Token usage (final chunk only)")
