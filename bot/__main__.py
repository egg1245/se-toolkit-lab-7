#!/usr/bin/env python3
"""Allow running as: python -m bot --test "/command" from bot/ directory
Or: uv run python -m bot --test "/command"
"""

import sys
import os

# Add parent directory so 'bot' package can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from bot.bot
from bot.bot import main

if __name__ == "__main__":
    main()
