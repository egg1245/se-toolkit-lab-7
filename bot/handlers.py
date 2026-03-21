"""DEPRECATED: This file is kept for compatibility. Use bot.handlers.commands instead.

This module is deprecated. All command handlers have moved to:
  bot.handlers.commands

Import from there:
  from bot.handlers import handle_start, handle_help, etc.
"""

# Backward compatibility re-exports (if needed)
from bot.handlers.commands import (
    handle_health,
    handle_help,
    handle_labs,
    handle_scores,
    handle_start,
)

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
]

