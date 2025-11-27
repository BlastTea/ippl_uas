"""Login helper that wraps the sigma backend login endpoint."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .http_client import post_json


def login(username: str, password: str) -> Tuple[int, Dict[str, Any]]:
    """Send login request and return (status_code, response_dict)."""

    payload = {"username": username, "password": password}
    return post_json("login", payload)
