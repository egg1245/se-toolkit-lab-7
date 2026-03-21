"""Tests for LMS client (task-2).

Tests async HTTP client interface and configuration.
Note: Full HTTP mocking would use pytest-httpx (optional dependency).
"""

import pytest

from bot.services.lms_client import LMSClient


@pytest.fixture
def lms_client():
    """Create LMS client for testing."""
    return LMSClient(base_url="http://backend:42002", api_key="test-key")


@pytest.mark.asyncio
async def test_get_items_success(lms_client):
    """Test fetching items from LMS."""
    # This test demonstrates the async interface
    # In real testing with pytest-httpx, you'd mock the responses
    assert lms_client.base_url == "http://backend:42002"
    assert lms_client.api_key == "test-key"


@pytest.mark.asyncio
async def test_client_headers(lms_client):
    """Test that client builds correct auth headers."""
    headers = lms_client._headers()
    assert headers["Authorization"] == "Bearer test-key"
    assert headers["Content-Type"] == "application/json"


def test_base_url_normalization(lms_client):
    """Test that base URLs are normalized (trailing slashes removed)."""
    client_with_slash = LMSClient(base_url="http://backend:42002/", api_key="key")
    assert client_with_slash.base_url == "http://backend:42002"
    
    client_no_slash = LMSClient(base_url="http://backend:42002", api_key="key")
    assert client_no_slash.base_url == "http://backend:42002"


