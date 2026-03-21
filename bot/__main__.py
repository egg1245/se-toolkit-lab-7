#!/usr/bin/env python3
"""Allow running as: python -m bot --test "/command" """

import sys
import os

# Add parent directory to path so imports work from bot/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.bot import main

if __name__ == "__main__":
    main()
