"""Boundary-value tests for login and refresh."""

from __future__ import annotations

import os

from load_dotenv import load_dotenv
from request.http_client import post_json

load_dotenv()

USERNAME = os.getenv("USERNAME_LOGIN", "")
PASSWORD = os.getenv("PASSWORD_LOGIN", "")


def check(desc: str, payload: dict, expected: int, endpoint: str) -> None:
    status, body = post_json(endpoint, payload)
    verdict = "PASS" if status == expected else "FAIL"
    print(f"{desc}: {status} (expected {expected}) -> {verdict}")
    if verdict == "FAIL":
        print("  response:", body)


def login_boundaries() -> None:
    print("=== LOGIN BOUNDARIES ===")
    cases = [
        ("Empty username", {"username": "", "password": PASSWORD}, 400),
        ("Valid credentials", {"username": USERNAME, "password": PASSWORD}, 200),
        ("Username + extra char", {"username": USERNAME + "_", "password": PASSWORD}, 401),
        ("Password missing char", {"username": USERNAME, "password": PASSWORD[:-1]}, 401),
        ("Password + extra char", {"username": USERNAME, "password": PASSWORD + "!"}, 401),
    ]
    for desc, payload, expected in cases:
        check(desc, payload, expected, "login")


def refresh_boundaries() -> None:
    print("\n=== REFRESH BOUNDARIES ===")
    status, body = post_json("login", {"username": USERNAME, "password": PASSWORD})
    token = body.get("data", {}).get("refresh_token") if status == 200 else ""

    cases = [
        ("Empty token", {"refresh_token": ""}, 400),
        ("Valid token", {"refresh_token": token}, 200),
        ("Token missing char", {"refresh_token": token[:-1]}, 401),
        ("Token + extra char", {"refresh_token": token + "x"}, 401),
    ]
    for desc, payload, expected in cases:
        check(desc, payload, expected, "token/refresh")


if __name__ == "__main__":
    login_boundaries()
    refresh_boundaries()
