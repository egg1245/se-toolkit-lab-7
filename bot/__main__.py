#!/usr/bin/env python3
"""Allow running as: python -m bot --test "/command" from bot/ directory"""

import sys
import os

# Ensure parent directory is in path for imports from bot/
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from bot.bot import main

if __name__ == "__main__":
    main()
