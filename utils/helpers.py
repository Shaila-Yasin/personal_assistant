"""
utils/helpers.py

Small, generic helper functions used across the app. Nothing in here
should know about conversations, Groq, or the CLI — these are pure
utility functions.
"""

import uuid
from datetime import datetime


def generate_id() -> str:
    """Generate a short unique id, e.g. '6f2d8c1a'. Used to name conversation files."""
    return uuid.uuid4().hex[:8]


def now_timestamp() -> str:
    """Return the current time as an ISO-8601 string, e.g. '2026-07-08T14:32:01'."""
    return datetime.now().isoformat(timespec="seconds")


def format_timestamp(iso_string: str) -> str:
    """Turn an ISO timestamp into something more human-readable for the CLI."""
    try:
        dt = datetime.fromisoformat(iso_string)
        return dt.strftime("%b %d, %Y %I:%M %p")
    except ValueError:
        return iso_string


def is_valid_input(user_input: str) -> bool:
    """Reject empty or whitespace-only input before sending it to the model."""
    return bool(user_input and user_input.strip())
