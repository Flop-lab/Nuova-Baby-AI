"""Structured logging setup for Baby AI"""
import structlog
import logging
import sys
import os

# Define a log directory and ensure it exists
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, "baby_ai.jsonl")


def setup_logging(log_level: str = "INFO"):
    """
    Configure structured logging to output to both console and a file.
    This setup is robust and safe for hot-reloading environments like Uvicorn.
    """
    # Shared processors for consistent log structure
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # --- Formatter Definitions ---
    # Formatter for the console with colored output
    console_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer(colors=True),
    )

    # Formatter for the file with JSON output
    file_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
    )

    # --- Handler Definitions ---
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    # File handler (mode 'a' for appending)
    file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8")
    file_handler.setFormatter(file_formatter)

    # --- Root Logger Configuration ---
    root_logger = logging.getLogger()

    # ** CRITICAL STEP for hot-reloading environments **
    # Clear any existing handlers to prevent duplicate log entries
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Add the configured handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(log_level.upper())

    logger = structlog.get_logger("baby_ai")
    logger.info("Logging configured successfully", console_output=True, file_output=LOG_FILE_PATH)
