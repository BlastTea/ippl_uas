"""Boundary value tests for login and refresh endpoints"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Tuple

from load_dotenv import load_dotenv
from request.http_client import post_json

load_dotenv()

USERNAME = os.getenv("USERNAME_LOGIN")
PASSWORD = os.getenv("PASSWORD_LOGIN")

if not USERNAME or not PASSWORD:
    raise RuntimeError("USERNAME_LOGIN and PASSWORD_LOGIN must be set in .env")


Caller = Callable[[Dict[str, Any]], Tuple[int, Dict[str, Any]]]
PayloadFactory = Callable[[], Dict[str, Any]]


def _login_call(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    return post_json("login", payload)


def _refresh_call(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    return post_json("token/refresh", payload)


def _short_password() -> str:
    if len(PASSWORD) > 1:
        return PASSWORD[:-1]
    return ""


def _valid_refresh_token() -> str:
    status, body = _login_call({"username": USERNAME, "password": PASSWORD})
    if status != 200:
        raise RuntimeError(f"Unable to obtain refresh token (status {status}, body={body})")

    data = body.get("data", {})
    token = data.get("refresh_token")
    if not token:
        raise RuntimeError("Login response missing refresh_token")
    return token


def _short_refresh_token() -> str:
    token = _valid_refresh_token()
    if len(token) <= 1:
        return ""
    return token[:-1]


def _long_refresh_token() -> str:
    token = _valid_refresh_token()
    if not token:
        return "A"
    return token + token[-1]


@dataclass
class BoundaryCase:
    label: str
    description: str
    expected_status: int
    payload_factory: PayloadFactory
    caller: Caller


def _run_cases(title: str, cases: List[BoundaryCase]) -> None:
    print(f"=== {title} ===")
    for case in cases:
        print(f"[{case.label}] {case.description}")
        payload = case.payload_factory()
        status, body = case.caller(payload)
        result = "PASS" if status == case.expected_status else "FAIL"
        print(f"  -> status {status} (expected {case.expected_status}) : {result}")
        if result == "FAIL":
            print(f"     response: {body}")


def login_boundary_cases() -> List[BoundaryCase]:
    return [
        BoundaryCase(
            label="B-L1",
            description="Username empty (below lower bound)",
            expected_status=400,
            payload_factory=lambda: {"username": "", "password": PASSWORD},
            caller=_login_call,
        ),
        BoundaryCase(
            label="B-L2",
            description="Valid credentials (on the boundary)",
            expected_status=200,
            payload_factory=lambda: {"username": USERNAME, "password": PASSWORD},
            caller=_login_call,
        ),
        BoundaryCase(
            label="B-L3",
            description="Username just beyond boundary (extra char)",
            expected_status=401,
            payload_factory=lambda: {"username": USERNAME + "_", "password": PASSWORD},
            caller=_login_call,
        ),
        BoundaryCase(
            label="B-L4",
            description="Password just below boundary (missing last char)",
            expected_status=400 if len(PASSWORD) == 1 else 401,
            payload_factory=lambda: {"username": USERNAME, "password": _short_password()},
            caller=_login_call,
        ),
        BoundaryCase(
            label="B-L5",
            description="Password just beyond boundary (extra char)",
            expected_status=401,
            payload_factory=lambda: {"username": USERNAME, "password": PASSWORD + "!"},
            caller=_login_call,
        ),
    ]


def refresh_boundary_cases() -> List[BoundaryCase]:
    return [
        BoundaryCase(
            label="B-R1",
            description="Empty token (below lower bound)",
            expected_status=400,
            payload_factory=lambda: {"refresh_token": ""},
            caller=_refresh_call,
        ),
        BoundaryCase(
            label="B-R2",
            description="Valid token (on the boundary)",
            expected_status=200,
            payload_factory=lambda: {"refresh_token": _valid_refresh_token()},
            caller=_refresh_call,
        ),
        BoundaryCase(
            label="B-R3",
            description="Token just below boundary (missing last char)",
            expected_status=401,
            payload_factory=lambda: {"refresh_token": _short_refresh_token()},
            caller=_refresh_call,
        ),
        BoundaryCase(
            label="B-R4",
            description="Token just beyond boundary (extra char)",
            expected_status=401,
            payload_factory=lambda: {"refresh_token": _long_refresh_token()},
            caller=_refresh_call,
        ),
    ]


def main() -> None:
    _run_cases("LOGIN BOUNDARY TESTS", login_boundary_cases())
    print()
    _run_cases("REFRESH BOUNDARY TESTS", refresh_boundary_cases())


if __name__ == "__main__":
    main()
