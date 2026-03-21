#!/usr/bin/env python3
"""Allow running as: python -m bot --test "/command"
Works in: local dev, docker, or uv run.
"""

from bot.bot import main

if __name__ == "__main__":
    main()
