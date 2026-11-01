"""
Structured logging configuration.

Provides consistent, structured logging across the application.
Ensures no secrets or sensitive data are logged.
"""

import logging
import sys
from datetime import datetime, timezone
from typing import Optional


# Patterns that indicate sensitive data
SENSITIVE_PATTERNS = [
    "api_key",
    "api-key",
    "apikey",
    "password",
    "secret",
    "token",
    "authorization",
    "auth",
    "credential",
    "ncbi_api_key",
    "llm_api_key",
]


class SanitizingFormatter(logging.Formatter):
    """Custom formatter that sanitizes sensitive data from log messages."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record, masking any sensitive data."""
        message = super().format(record)
        return self._sanitize(message)

    @staticmethod
    def _sanitize(message: str) -> str:
        """Mask sensitive values in log messages."""
        for pattern in SENSITIVE_PATTERNS:
            # Match patterns like api_key=VALUE or "api_key": "VALUE"
            import re

            # key=value pattern
            message = re.sub(
                rf"({pattern}\s*[=:]\s*)['\"]?[\w\-./]+['\"]?",
                rf"\1***MASKED***",
                message,
                flags=re.IGNORECASE,
            )
        return message


class StructuredLogger:
    """Provides structured logging with context."""

    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs) -> None:
        """Log info message with optional context."""
        self.logger.info(self._format_structured(message, **kwargs))

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message with optional context."""
        self.logger.warning(self._format_structured(message, **kwargs))

    def error(self, message: str, **kwargs) -> None:
        """Log error message with optional context."""
        self.logger.error(self._format_structured(message, **kwargs))

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message with optional context."""
        self.logger.debug(self._format_structured(message, **kwargs))

    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        self.logger.exception(self._format_structured(message, **kwargs))

    @staticmethod
    def _format_structured(message: str, **kwargs) -> str:
        """Format message with structured context."""
        if not kwargs:
            return message
        context = " ".join(f"{k}={v}" for k, v in kwargs.items())
        return f"{message} | {context}"


def setup_logging(debug: bool = False) -> None:
    """Configure application logging."""
    level = logging.DEBUG if debug else logging.INFO

    # Create sanitizing formatter
    formatter = SanitizingFormatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.DEBUG if debug else logging.WARNING
    )


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance."""
    return StructuredLogger(name)
