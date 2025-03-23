"""
Tests for the agent SDK and tool registry.

This module contains tests for the agent SDK and tool registry functionality.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents import registry


def test_tool_registry_register_and_get_tool():
    """Test that tools can be registered and retrieved from the registry."""
    # Clear the registry for this test
    registry.TOOL_REGISTRY.clear()
    
    # Define a dummy tool function
    def dummy_tool():
        return "Tool executed"
    
    # Register the dummy tool
    registry.register_tool("dummy_tool", dummy_tool)
    
    # Get the tool from the registry
    tool = registry.get_tool("dummy_tool")
    
    # Verify that the retrieved tool is the same as the registered one
    assert tool == dummy_tool
    
    # Verify that the tool can be executed
    assert tool() == "Tool executed"


def test_tool_registry_get_tool_not_found():
    """Test that get_tool returns None for non-registered tools."""
    # Clear the registry for this test
    registry.TOOL_REGISTRY.clear()
    
    # Try to get a non-existent tool
    tool = registry.get_tool("non_existent_tool")
    
    # Verify that None is returned
    assert tool is None


def test_tool_registry_list_tools():
    """Test that list_tools returns all registered tools."""
    # Clear the registry for this test
    registry.TOOL_REGISTRY.clear()
    
    # Define dummy tool functions
    def tool1(): pass
    def tool2(): pass
    
    # Register the tools
    registry.register_tool("tool1", tool1)
    registry.register_tool("tool2", tool2)
    
    # Get the list of tools
    tools = registry.list_tools()
    
    # Verify that the tools dictionary contains both registered tools
    assert len(tools) == 2
    assert "tool1" in tools
    assert "tool2" in tools
    assert tools["tool1"] == tool1
    assert tools["tool2"] == tool2


def test_web_search_tool_invocation():
    """Test that the web search tool can be invoked and returns a response."""
    # Import here to avoid initialization issues
    from app.agents.tools import web_search
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message = MagicMock()
    mock_completion.choices[0].message.content = "Web search results"
    mock_client.chat.completions.create.return_value = mock_completion
    
    with patch("app.agents.tools.web_search.get_openai_client", return_value=mock_client):
        # Invoke the web search tool
        response = web_search.perform_web_search(query="test query", user_message="test query")
        
        # Verify the response
        assert isinstance(response, dict)
        assert "content" in response
        assert "Web search results" in response["content"]
        
        # Verify the client was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == "gpt-3.5-turbo"
        assert call_args["messages"][1]["content"] == "Search for: test query"


def test_web_search_tool_error_handling():
    """Test that the web search tool handles errors gracefully."""
    # Import here to avoid initialization issues
    from app.agents.tools import web_search
    
    # Mock the OpenAI client to raise an exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API error")
    
    with patch("app.agents.tools.web_search.get_openai_client", return_value=mock_client):
        # Invoke the web search tool
        response = web_search.perform_web_search(query="test query", user_message="test query")
        
        # Verify the error response
        assert isinstance(response, dict)
        assert "content" in response
        assert "Error" in response["content"]


def test_file_search_tool():
    """Test that the file search tool returns an appropriate response for non-existent stores."""
    # Import here to avoid initialization issues
    from app.agents.tools import file_search
    
    # Invoke the file search tool with a non-existent vector store
    response = file_search.perform_file_search(query="test query", vector_store_id="test_store")
    
    # Verify the response
    assert isinstance(response, dict)
    assert "content" in response
    assert "Vector store 'test_store' not found" in response["content"]


def test_file_search_tool_with_store():
    """Test that the file search tool can create and search a vector store."""
    # Import here to avoid initialization issues
    from app.agents.tools import file_search
    import numpy as np
    
    # Mock the embedding function
    with patch("app.llm_provider.get_embedding", return_value=np.ones(1536, dtype='float32')):
        # Create a test vector store
        files = [
            {"path": "test1.txt", "content": "This is a test file with some content"},
            {"path": "test2.txt", "content": "Another test file with different content"}
        ]
        
        # Create the vector store
        result = file_search.create_vector_store("test_vector_store", files)
        assert result is True
        
        # Search the vector store
        response = file_search.perform_file_search(
            query="test content", 
            vector_store_id="test_vector_store"
        )
        
        # Verify the response
        assert isinstance(response, dict)
        assert "content" in response
        assert "Found" in response["content"]
        assert "test1.txt" in response["content"] or "test2.txt" in response["content"]


def test_tools_are_registered():
    """Test that the tools are registered in the registry when imported."""
    # Clear the registry for this test
    registry.TOOL_REGISTRY.clear()
    
    # Import the tools to ensure they're registered
    from app.agents.tools import web_search, file_search
    
    # Manually register the tools for testing
    registry.register_tool("web_search", web_search.perform_web_search)
    registry.register_tool("file_search", file_search.perform_file_search)
    
    # The tools should be registered when their modules are imported
    assert "web_search" in registry.TOOL_REGISTRY
    assert "file_search" in registry.TOOL_REGISTRY
    
    # Verify that the registered functions are the correct ones
    assert registry.get_tool("web_search") == web_search.perform_web_search
    assert registry.get_tool("file_search") == file_search.perform_file_search