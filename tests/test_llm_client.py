"""Tests for LLM client (task-3).

Tests tool definitions and LLM routing interface.
"""

import pytest

from bot.services.llm_client import LLMClient


@pytest.fixture
def llm_client():
    """Create LLM client for testing."""
    return LLMClient(api_base_url="http://localhost:8000", api_key="test-key")


class TestLLMClient:
    """Test LLM client and tool calling."""

    def test_define_tools(self, llm_client):
        """Test that client defines available tools."""
        tools = llm_client.define_tools()
        assert len(tools) == 2

        tool_names = {tool.name for tool in tools}
        assert "get_labs" in tool_names
        assert "get_scores" in tool_names

    def test_tool_has_description(self, llm_client):
        """Test that tools have formal descriptions."""
        tools = llm_client.define_tools()
        for tool in tools:
            assert len(tool.description) > 0, f"Tool {tool.name} has no description"
            assert tool.input_schema is not None, f"Tool {tool.name} has no input_schema"

    def test_tool_input_schema(self, llm_client):
        """Test that tools have JSON schema for parameters."""
        tools = llm_client.define_tools()
        for tool in tools:
            schema = tool.input_schema
            assert "type" in schema
            assert "properties" in schema

    @pytest.mark.asyncio
    async def test_ask_llm(self, llm_client):
        """Test ask_llm interface."""
        result = await llm_client.ask_llm("What labs are available?")
        assert isinstance(result, dict)
        assert "tool" in result
        assert "params" in result
        assert "reasoning" in result

    def test_tool_descriptions_quality(self, llm_client):
        """Test that tool descriptions are detailed and specific."""
        tools = llm_client.define_tools()
        
        # Find get_labs tool
        get_labs = next(t for t in tools if t.name == "get_labs")
        # Should mention specific use cases
        assert any(word in get_labs.description.lower() 
                  for word in ["labs", "assignments", "courses"])
        
        # Find get_scores tool  
        get_scores = next(t for t in tools if t.name == "get_scores")
        # Should mention specific use cases
        assert any(word in get_scores.description.lower()
                  for word in ["score", "grades", "performance"])

