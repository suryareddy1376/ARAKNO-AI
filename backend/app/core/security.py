"""
Security utilities.

Provides path traversal prevention, file validation,
API key masking, and other security measures.
"""

import os
import re
from pathlib import Path
from typing import Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


def sanitize_path(base_dir: str, user_path: str) -> Path:
    """
    Safely resolve a user-provided path within a base directory.

    Prevents path traversal attacks by ensuring the resolved path
    stays within the base directory.

    Args:
        base_dir: The allowed base directory.
        user_path: The user-provided path component.

    Returns:
        Resolved safe path.

    Raises:
        ValueError: If the path attempts to traverse outside base_dir.
    """
    base = Path(base_dir).resolve()
    # Remove any potentially dangerous characters
    cleaned = re.sub(r"[^\w\s\-./]", "", user_path)
    # Resolve the full path
    target = (base / cleaned).resolve()

    # Verify the resolved path is within base directory
    if not str(target).startswith(str(base)):
        logger.warning(
            "Path traversal attempt detected",
            base_dir=str(base),
            attempted_path=user_path,
        )
        raise ValueError("Path traversal detected: path is outside allowed directory")

    return target


def validate_file_extension(filename: str, allowed_extensions: list[str]) -> bool:
    """
    Validate that a filename has an allowed extension.

    Args:
        filename: The filename to check.
        allowed_extensions: List of allowed extensions (e.g., ['.pdb', '.cif']).

    Returns:
        True if the extension is allowed.
    """
    ext = Path(filename).suffix.lower()
    return ext in [e.lower() for e in allowed_extensions]


def validate_file_size(size_bytes: int, max_size_bytes: int) -> bool:
    """
    Validate that a file size is within limits.

    Args:
        size_bytes: Actual file size in bytes.
        max_size_bytes: Maximum allowed size in bytes.

    Returns:
        True if within limits.
    """
    return 0 < size_bytes <= max_size_bytes


def mask_api_key(key: Optional[str]) -> str:
    """
    Mask an API key for safe display/logging.

    Shows only the first 4 and last 4 characters.

    Args:
        key: The API key to mask.

    Returns:
        Masked key string.
    """
    if not key:
        return "not_set"
    if len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to prevent injection attacks.

    Args:
        filename: The filename to sanitize.

    Returns:
        Sanitized filename.
    """
    # Remove path separators and null bytes
    cleaned = filename.replace("/", "_").replace("\\", "_").replace("\0", "")
    # Remove any non-alphanumeric characters except allowed ones
    cleaned = re.sub(r"[^\w\s\-.]", "_", cleaned)
    # Prevent hidden files
    cleaned = cleaned.lstrip(".")
    # Limit length
    if len(cleaned) > 255:
        name, ext = os.path.splitext(cleaned)
        cleaned = name[: 255 - len(ext)] + ext
    return cleaned or "unnamed"


def validate_content_type(
    content_type: Optional[str], allowed_types: list[str]
) -> bool:
    """
    Validate Content-Type header against allowed types.

    Args:
        content_type: The Content-Type value.
        allowed_types: List of allowed MIME types.

    Returns:
        True if the content type is allowed.
    """
    if not content_type:
        return False
    # Extract base type (ignore parameters like charset)
    base_type = content_type.split(";")[0].strip().lower()
    return base_type in [t.lower() for t in allowed_types]


def is_safe_url(url: str) -> bool:
    """
    Check if a URL is safe to make requests to.

    Prevents SSRF by blocking internal/private network URLs.

    Args:
        url: The URL to validate.

    Returns:
        True if the URL appears safe.
    """
    from urllib.parse import urlparse

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    # Must be http or https
    if parsed.scheme not in ("http", "https"):
        return False

    hostname = parsed.hostname
    if not hostname:
        return False

    # Block private/internal hostnames
    blocked_patterns = [
        "localhost",
        "127.",
        "10.",
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",
        "192.168.",
        "0.",
        "169.254.",
        "::1",
        "fe80:",
    ]

    hostname_lower = hostname.lower()
    for pattern in blocked_patterns:
        if hostname_lower.startswith(pattern) or hostname_lower == pattern.rstrip("."):
            return False

    return True
