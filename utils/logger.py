"""
utils/logger.py

Centralized logging setup. Instead of scattering print() statements
through the codebase for debugging, every module calls get_logger(__name__)
and logs through that.

Logs go to logs/app.log (created automatically) so you can inspect what
happened after the fact, without cluttering the CLI's chat output.
"""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


def get_logger(name: str) -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger() is called
    # multiple times for the same module (e.g. on re-import).
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
