from pydantic import BaseModel, Field

class OrchestratorConfig(BaseModel):
    """Configuration for orchestrator behavior"""
    max_validation_retries: int = Field(default=3, description="Max retries for validation errors")
    llm_timeout_seconds: int = Field(default=30, description="LLM request timeout")
    enable_streaming: bool = Field(default=True, description="Enable streaming responses")
