"""Logging setup for Module 3: File Handling, Exceptions and Database Connectivity.
This module writes timestamped technical details to the shared application log.
"""

import logging
import os

import settings

# CHANGE ME: change the level here when a live demo needs more or less detail.
LOG_LEVEL = logging.INFO

# CONCEPT: Logging


def setup_logging():
    """Create the log directory and configure the standard logging module."""
    folder = os.path.dirname(settings.LOG_FILE)
    if folder:
        os.makedirs(folder, exist_ok=True)
    logging.basicConfig(
        filename=settings.LOG_FILE,
        level=LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def demo():
    """Write one message at each useful demo level and display recent lines."""
    setup_logging()
    logging.info("Module 3 information example")
    logging.warning("Module 3 warning example")
    logging.error("Module 3 error example")
    with open(settings.LOG_FILE, "r", encoding="utf-8") as log_file:
        lines = log_file.readlines()
    print("Last log lines:")
    for line in lines[-3:]:
        print(line.rstrip())


if __name__ == "__main__":
    demo()
