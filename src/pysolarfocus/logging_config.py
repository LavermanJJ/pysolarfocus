"""Logging configuration for pysolarfocus"""

import logging
import sys
from typing import Optional


def setup_logging(level: int = logging.INFO, format_string: Optional[str] = None, filename: Optional[str] = None) -> None:
    """Setup logging configuration for pysolarfocus.

    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string for log messages
        filename: Optional filename to log to file instead of console
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure basic logging
    if filename:
        logging.basicConfig(level=level, format=format_string, filename=filename, filemode="a")
    else:
        logging.basicConfig(level=level, format=format_string, stream=sys.stdout)

    # Set specific logger for pysolarfocus
    logger = logging.getLogger("pysolarfocus")
    logger.setLevel(level)

    # Reduce noise from pymodbus if not in debug mode
    if level > logging.DEBUG:
        logging.getLogger("pymodbus").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for pysolarfocus modules.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"pysolarfocus.{name}")
