"""Refresh token helper for the sigma backend."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .http_client import post_json


def refresh(refresh_token: str) -> Tuple[int, Dict[str, Any]]:
    """Send refresh token request and return (status_code, response_dict)."""

    payload = {"refresh_token": refresh_token}
    return post_json("token/refresh", payload)
