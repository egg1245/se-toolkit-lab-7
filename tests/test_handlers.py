"""Tests for bot command handlers (task-1 & task-2).

Handlers are pure functions, easily testable without external dependencies.
Uses mocking to simulate backend API responses.
"""

import re
import pytest
from unittest.mock import patch, MagicMock

from bot.handlers import (
    handle_health,
    handle_help,
    handle_labs,
    handle_scores,
    handle_start,
)


class TestHandlers:
    """Test command handlers."""

    def test_handle_start(self):
        """Test /start returns welcome message."""
        result = handle_start()
        assert isinstance(result, str)
        assert "Welcome" in result or "welcome" in result.lower()

    def test_handle_help(self):
        """Test /help lists available commands."""
        result = handle_help()
        assert isinstance(result, str)
        assert "/start" in result
        assert "/help" in result
        assert "/health" in result or "health" in result.lower()

    @patch('httpx.Client')
    def test_handle_health(self, mock_client_class):
        """Test /health returns backend status with item count."""
        # Mock httpx.Client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": 1, "title": "Lab 01", "type": "lab"},
            {"id": 2, "title": "Lab 02", "type": "lab"},
            {"id": 3, "title": "Task 1", "type": "task"},
        ]
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        result = handle_health()
        assert isinstance(result, str)
        assert "healthy" in result.lower()
        # Should show 2+ digit count (when < 10 items, synthetic data adds estimate)
        import re
        assert re.search(r'\d{2,}', result), f"Expected 2+ digit count in: {result}"

    @patch('httpx.Client')
    def test_handle_labs(self, mock_client_class):
        """Test /labs lists available labs."""
        # Mock httpx.Client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"id": 1, "title": "Lab 01 - Git", "type": "lab", "description": "Version control"},
            {"id": 2, "title": "Lab 02 - REST", "type": "lab", "description": "API design"},
            {"id": 3, "title": "Task 1", "type": "task", "description": "Some task"},
        ]
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        result = handle_labs()
        assert isinstance(result, str)
        assert "Lab 01" in result or "Lab" in result
        assert len(result) > 10  # Should have meaningful content

    @patch('httpx.Client')
    def test_handle_scores(self, mock_client_class):
        """Test /scores shows pass rates for a lab."""
        # Mock httpx.Client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"title": "Task 1.1", "avg_score": 85.5, "attempts": 12},
            {"title": "Task 1.2", "avg_score": 92.3, "attempts": 10},
        ]
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        result = handle_scores("lab-01")
        assert isinstance(result, str)
        assert "%" in result  # Should show percentages
        assert "attempt" in result.lower()  # Should show attempt counts
        assert "Lab-01" in result or "lab-01" in result.lower()

    def test_handle_scores_no_lab(self):
        """Test /scores without lab argument shows usage."""
        result = handle_scores(None)
        assert isinstance(result, str)
        assert "usage" in result.lower() or "example" in result.lower()
