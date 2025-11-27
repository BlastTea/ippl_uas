"""Minimal HTTP helper for talking to the sigma backend."""

from __future__ import annotations

import json
import os

from typing import Any, Dict, Tuple
from urllib import error, request
from urllib.parse import urljoin

_base_url_raw = os.getenv("URL")
if not _base_url_raw:
    raise RuntimeError("URL is not configured. Please provide it in .env")

_base_url = _base_url_raw.rstrip("/") + "/"

try:
    _timeout = float(os.getenv("TIMEOUT", "10"))
except ValueError:
    _timeout = 10.0


def post_json(path: str, payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """POST JSON payload to the backend and return status plus parsed body."""

    url = urljoin(_base_url, path.lstrip("/"))
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, data=data, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with request.urlopen(req, timeout=_timeout) as resp:
            status = resp.getcode() or 0
            body = resp.read()
    except error.HTTPError as exc:
        status = exc.code
        body = exc.read()
    except error.URLError as exc:
        return 0, {"error": str(getattr(exc, "reason", exc))}

    return status, _parse_body(body)


def _parse_body(raw: bytes) -> Dict[str, Any]:
    if not raw:
        return {}

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return {"raw": raw.decode("utf-8", errors="replace")}

    if isinstance(parsed, dict):
        return parsed

    return {"data": parsed}
