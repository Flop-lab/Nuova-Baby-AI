import pytest
from src.agents.app_agent import AppAgent
from src.models.schemas import ToolCall, FunctionCall

# Test 1: get_tools returns correct tool definitions
def test_get_tools():
    tools = AppAgent.get_tools()
    assert isinstance(tools, list)
    assert any(tool["name"] == "open_app" for tool in tools)
    assert any(tool["name"] == "close_app" for tool in tools)
    for tool in tools:
        assert "appName" in tool["parameters"]

# Test 2: execute handles unknown function gracefully
def test_execute_unknown_function():
    agent = AppAgent()
    tool_call = ToolCall(function=FunctionCall(name="not_a_function", arguments={"appName": "Safari"}))
    result = agent.execute(tool_call)
    assert not result.success
    assert "Unknown function" in result.error

# Test 3: execute handles missing appName argument
def test_execute_missing_appname():
    agent = AppAgent()
    tool_call = ToolCall(function=FunctionCall(name="open_app", arguments={}))
    result = agent.execute(tool_call)
    assert not result.success
    assert result.error is not None
