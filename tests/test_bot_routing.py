"""Tests for bot command routing (task-1 integration)."""

import pytest

from bot.bot import parse_command, route_message


class TestBotRouting:
    """Test command parsing and routing."""

    def test_parse_command_simple(self):
        """Test parsing simple command."""
        cmd, args = parse_command("/start")
        assert cmd == "/start"
        assert args == ""

    def test_parse_command_with_args(self):
        """Test parsing command with arguments."""
        cmd, args = parse_command("/get some args here")
        assert cmd == "/get"
        assert args == "some args here"

    def test_route_message_start(self):
        """Test routing /start command."""
        result = route_message("/start")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_route_message_help(self):
        """Test routing /help command."""
        result = route_message("/help")
        assert isinstance(result, str)
        assert "/start" in result or "start" in result.lower()

    def test_route_message_unknown(self):
        """Test routing unknown command."""
        result = route_message("/notacommand")
        assert isinstance(result, str)
        assert "unknown" in result.lower() or "not recognized" in result.lower()

