#!/usr/bin/env python3
"""Telegram bot entry point with --test mode for debugging.

Usage:
  cd bot && uv run python3 bot.py --test "/start"
  cd bot && uv run python3 bot.py --test "/help"
  
Or production: uv run python -m bot.bot (Telegram polling mode)
"""

import argparse
import asyncio
import os
import sys
import logging

# Ensure bot package is importable when running from bot/ directory
if os.path.dirname(os.path.dirname(os.path.abspath(__file__))) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.handlers import handle_health, handle_help, handle_labs, handle_scores, handle_start
from bot.config import load_config

# Telegram bot imports
try:
    from telegram import Update, BotCommand
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    pass

logging.basicConfig(level=logging.INFO)


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
    
    # Production mode: start Telegram polling
    try:
        config = load_config(".env.bot.secret")
        # Run the async bot
        import nest_asyncio
        nest_asyncio.apply()  # Allow nested event loops
        asyncio.run(run_telegram_bot(config.telegram_token))
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error starting bot: {e}", exc_info=True)
        sys.exit(1)


async def run_telegram_bot(token: str):
    """Run the Telegram bot with polling."""
    app = Application.builder().token(token).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", telegram_start))
    app.add_handler(CommandHandler("help", telegram_help))
    app.add_handler(CommandHandler("health", telegram_health))
    app.add_handler(CommandHandler("labs", telegram_labs))
    app.add_handler(CommandHandler("scores", telegram_scores))
    
    # Start polling
    logging.info("Bot started polling...")
    await app.run_polling()


async def telegram_start(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
    """Handle /start command."""
    text = handle_start()
    await update.message.reply_text(text)


async def telegram_help(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
    """Handle /help command."""
    text = handle_help()
    await update.message.reply_text(text)


async def telegram_health(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
    """Handle /health command."""
    text = handle_health()
    await update.message.reply_text(text)


async def telegram_labs(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
    """Handle /labs command."""
    text = handle_labs()
    await update.message.reply_text(text)


async def telegram_scores(update: "Update", context: "ContextTypes.DEFAULT_TYPE") -> None:
    """Handle /scores command."""
    args = " ".join(context.args) if context.args else ""
    text = handle_scores(args) if args else handle_scores()
    await update.message.reply_text(text)


if __name__ == "__main__":
    main()
