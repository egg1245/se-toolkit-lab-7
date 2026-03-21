"""Tests for bot command handlers (task-1).

Handlers are pure functions, easily testable without external dependencies.
"""

import pytest

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

    def test_handle_health(self):
        """Test /health returns status."""
        result = handle_health()
        assert isinstance(result, str)
        assert "healthy" in result.lower() or "running" in result.lower()

    def test_handle_labs(self):
        """Test /labs returns message (placeholder in task-1)."""
        result = handle_labs()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_handle_scores(self):
        """Test /scores returns message (placeholder in task-1)."""
        result = handle_scores()
        assert isinstance(result, str)
        assert len(result) > 0

