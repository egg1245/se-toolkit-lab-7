#!/usr/bin/env python3
"""Simple wrapper to run from bot directory: cd bot && python bot.py --test "/start"

This script adjusts the path so bot can import from bot.handlers/services
"""

import sys
import os

# Add parent directory to path so 'bot' package is found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import and run bot.bot.main
if __name__ == "__main__":
    from bot.bot import main
    main()
