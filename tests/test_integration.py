"""
Simple integration tests for basic component functionality.
Focus on testing what we have implemented so far.
"""

import pytest
import json
from unittest.mock import Mock, patch
from src.models.schemas import ToolCall, FunctionCall, ExecutionResult, ChatRequest, ChatResponse
from src.agents.app_agent import AppAgent
from src.llm.ollama_adapter import OllamaAdapter


class TestBasicIntegration:
    """Test basic integration between components."""
    
    def test_app_agent_tool_execution_success(self):
        """Test successful tool execution in AppAgent."""
        agent = AppAgent()
        
        # Create valid tool call
        tool_call = ToolCall(
            function=FunctionCall(
                name="open_app",
                arguments={"appName": "TextEdit"}
            )
        )
        
        # Mock subprocess to simulate successful app opening
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = Mock(returncode=0)
            
            result = agent.execute(tool_call)
            
            # Verify execution result
            assert isinstance(result, ExecutionResult)
            assert result.success is True
            assert result.error is None
            assert result.duration_ms > 0

    def test_app_agent_tool_execution_failure(self):
        """Test failed tool execution handling."""
        agent = AppAgent()
        
        # Create tool call for non-existent app
        tool_call = ToolCall(
            function=FunctionCall(
                name="open_app", 
                arguments={"appName": "NonExistentApp"}
            )
        )
        
        # Mock subprocess to simulate failure
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = Mock(returncode=1)
            
            result = agent.execute(tool_call)
            
            # Verify failure is handled gracefully
            assert isinstance(result, ExecutionResult)
            assert result.success is False
            assert result.error is not None
            assert "NonExistentApp" in result.error

    def test_app_agent_invalid_tool_call(self):
        """Test handling of invalid tool calls."""
        agent = AppAgent()
        
        # Create invalid tool call
        tool_call = ToolCall(
            function=FunctionCall(
                name="invalid_function",
                arguments={"appName": "TestApp"}  # Valid appName but invalid function
            )
        )
        
        result = agent.execute(tool_call)
        
        # Verify invalid tool is rejected
        assert isinstance(result, ExecutionResult)
        assert result.success is False
        assert "Unknown function" in result.error

    def test_tool_schema_validation(self):
        """Test that tool schemas are properly structured."""
        tools = AppAgent.get_tools()
        
        # Verify tool count and structure
        assert len(tools) == 2
        tool_names = [tool["name"] for tool in tools]
        assert "open_app" in tool_names
        assert "close_app" in tool_names
        
        # Verify each tool has basic structure
        for tool in tools:
            assert "name" in tool
            assert "description" in tool
            assert "parameters" in tool
            assert "required" in tool

    def test_chat_request_validation(self):
        """Test ChatRequest schema validation."""
        # Valid request
        request = ChatRequest(message="Open Safari")
        assert request.message == "Open Safari"
        assert request.stream is False
        
        # Request with streaming
        stream_request = ChatRequest(message="Hello", stream=True)
        assert stream_request.stream is True

    def test_chat_response_creation(self):
        """Test ChatResponse creation and validation."""
        response = ChatResponse(reply="I've opened Safari for you!")
        assert response.reply == "I've opened Safari for you!"
        assert response.trace is None

    def test_tool_call_json_serialization(self):
        """Test that ToolCall objects can be serialized to JSON."""
        tool_call = ToolCall(
            id="test-123",
            function=FunctionCall(
                name="open_app",
                arguments={"appName": "Safari"}
            )
        )
        
        # Should serialize without error
        json_str = tool_call.model_dump_json()
        data = json.loads(json_str)
        
        assert data["function"]["name"] == "open_app"
        assert data["function"]["arguments"]["appName"] == "Safari"

    def test_execution_result_timing(self):
        """Test that ExecutionResult includes timing information."""
        agent = AppAgent()
        
        tool_call = ToolCall(
            function=FunctionCall(
                name="open_app",
                arguments={"appName": "Calculator"}
            )
        )
        
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = Mock(returncode=0)
            
            result = agent.execute(tool_call)
            
            # Verify timing is captured
            assert result.duration_ms > 0
            assert isinstance(result.duration_ms, float)

    @patch('ollama.generate')
    def test_ollama_adapter_integration(self, mock_generate):
        """Test OllamaAdapter basic functionality."""
        # Mock ollama response
        mock_generate.return_value = {
            "message": {
                "content": "I'll help you open that application!"
            }
        }
        
        adapter = OllamaAdapter(model="qwen3:4b-thinking-2507-q8_0")
        result = adapter.generate("Open TextEdit")
        
        # Verify adapter returns structured response
        assert isinstance(result, dict)
        assert "message" in result
        
        # Verify ollama was called
        mock_generate.assert_called_once()

    def test_app_agent_close_app_functionality(self):
        """Test close_app tool execution."""
        agent = AppAgent()
        
        tool_call = ToolCall(
            function=FunctionCall(
                name="close_app",
                arguments={"appName": "Safari"}
            )
        )
        
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value = Mock(returncode=0)
            
            result = agent.execute(tool_call)
            
            # Verify execution success
            assert result.success is True

    def test_error_handling_chain(self):
        """Test error propagation through component chain."""
        agent = AppAgent()
        
        # Test missing required argument
        tool_call = ToolCall(
            function=FunctionCall(
                name="open_app",
                arguments={}  # Missing appName
            )
        )
        
        result = agent.execute(tool_call)
        
        # Verify error is properly captured and formatted
        assert result.success is False
        assert result.error is not None
        assert isinstance(result.error, str)
        assert len(result.error) > 0