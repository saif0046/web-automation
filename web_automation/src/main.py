"""
Main Runner File
----------------
Entry point of the entire project.
"""

import asyncio
from src.core.solver import solve_captcha
from src.utils.logger import get_logger

logger = get_logger("main")

if __name__ == "__main__":
    ok, text = asyncio.run(solve_captcha(headless=False))
    if ok:
        logger.info(f"SUCCESS → CAPTCHA solved: {text}")
    else:
        logger.error("FAILED → CAPTCHA not solved")
