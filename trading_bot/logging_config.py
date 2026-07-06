"""Logging configuration for trading bot."""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(log_file: str = "logs/trading_bot.log") -> logging.Logger:
    """
    Configure logging for the trading bot.

    Args:
        log_file: Path to the log file.

    Returns:
        Configured logger instance.
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create logger
    logger = logging.getLogger("trading_bot")
    logger.setLevel(logging.DEBUG)

    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    simple_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler (detailed logging)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB per file, keep 5 backups
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler (simple logging)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger() -> logging.Logger:
    """
    Get the configured logger.

    Returns:
        Logger instance.
    """
    return logging.getLogger("trading_bot")
