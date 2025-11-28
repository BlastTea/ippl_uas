"""Combinatorial testing driver for login and refresh parameters."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple

import os

from load_dotenv import load_dotenv
from request.http_client import post_json

load_dotenv()

USERNAME = os.getenv("USERNAME_LOGIN")
PASSWORD = os.getenv("PASSWORD_LOGIN")


def _login_call(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    return post_json("login", payload)


def _refresh_call(payload: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    return post_json("token/refresh", payload)


def _refresh_token() -> str:
    status, body = _login_call({"username": USERNAME, "password": PASSWORD})
    if status != 200:
        raise RuntimeError(f"Cannot fetch refresh token: {body}")
    token = body.get("data", {}).get("refresh_token")
    if not token:
        raise RuntimeError("Login response missing refresh_token")
    return token


def _combinations_login() -> List[Tuple[str, Dict[str, Any], int]]:
    return [
        ("valid username, valid password", {"username": USERNAME, "password": PASSWORD}, 200),
        ("valid username, wrong password", {"username": USERNAME, "password": "wrong"}, 401),
        ("unknown username, valid password", {"username": "unknown", "password": PASSWORD}, 401),
        ("empty username, valid password", {"username": "", "password": PASSWORD}, 400),
        ("valid username, empty password", {"username": USERNAME, "password": ""}, 400),
    ]


def _combinations_refresh(token: str) -> List[Tuple[str, Dict[str, Any], int]]:
    return [
        ("valid token", {"refresh_token": token}, 200),
        ("missing token", {}, 400),
        ("empty token", {"refresh_token": ""}, 400),
        ("random token", {"refresh_token": "XYZ"}, 401),
    ]


def _run_combinations(title: str, combos: List[Tuple[str, Dict[str, Any], int]], caller: Callable[[Dict[str, Any]], Tuple[int, Dict[str, Any]]]) -> None:
    print(f"=== {title} ===")
    for idx, (desc, payload, expected) in enumerate(combos, 1):
        status, body = caller(payload)
        verdict = "PASS" if status == expected else "FAIL"
        print(f"[{idx}] {desc}")
        print(f"    status {status} (expected {expected}) => {verdict}")
        if verdict == "FAIL":
            print(f"    response: {body}")


def main() -> None:
    token = _refresh_token()

    login_combos = _combinations_login()
    refresh_combos = _combinations_refresh(token)

    _run_combinations("LOGIN COMBINATORIAL CASES", login_combos, _login_call)
    print()
    _run_combinations("REFRESH COMBINATORIAL CASES", refresh_combos, _refresh_call)


if __name__ == "__main__":
    main()
