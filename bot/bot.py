#!/usr/bin/env python3
"""Telegram bot entry point with --test mode for debugging.

Usage:
  cd bot && uv run bot.py --test "/start"
  cd bot && uv run bot.py --test "/help"
  
Production usage: Telegram polling would be implemented here (not included in MVP).
"""

import argparse
import sys
import os

# Ensure bot package is importable when running from bot/ directory
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.handlers import handle_health, handle_help, handle_labs, handle_scores, handle_start


def parse_command(text: str) -> tuple[str, str]:
    """Parse command and arguments from user input.
    
    Args:
        text: User input (e.g., "/start" or "/get something").
        
    Returns:
        Tuple of (command, args).
    """
    parts = text.strip().split(maxsplit=1)
    if not parts:
        return "", ""
    return parts[0], (parts[1] if len(parts) > 1 else "")


def route_message(command: str, args: str = "") -> str:
    """Route command to appropriate handler.
    
    Args:
        command: Command name (e.g., "/start").
        args: Optional arguments.
        
    Returns:
        Handler response as string.
    """
    handlers = {
        "/start": lambda _: handle_start(),
        "/help": lambda _: handle_help(),
        "/health": lambda _: handle_health(),
        "/labs": lambda _: handle_labs(),
        "/scores": lambda _: handle_scores(),
    }
    
    if command in handlers:
        return handlers[command](args)
    
    return f"Unknown command: {command}. Use /help for available commands."


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="COMMAND",
        help="Run command in test mode (e.g., --test '/start')",
    )
    
    args = parser.parse_args()
    
    if args.test:
        # Test mode: parse and route command
        command, cmd_args = parse_command(args.test)
        response = route_message(command, cmd_args)
        print(response)
        sys.exit(0)
    
    # Production mode would be implemented here (Telegram polling)
    print("Production mode not implemented yet. Use --test mode.")
    sys.exit(1)


if __name__ == "__main__":
    main()
