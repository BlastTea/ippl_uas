"""Simple combinatorial matrix for login + refresh."""

from __future__ import annotations

import os

from load_dotenv import load_dotenv
from request.http_client import post_json

load_dotenv()

USERNAME = os.getenv("USERNAME_LOGIN", "")
PASSWORD = os.getenv("PASSWORD_LOGIN", "")


def run_cases(title: str, endpoint: str, combos: list[tuple[str, dict, int]]) -> None:
    print(f"=== {title} ===")
    for desc, payload, expected in combos:
        status, _ = post_json(endpoint, payload)
        print(f"{desc}: {status} (expected {expected})")


def main() -> None:
    login_combos = [
        ("valid user + valid pass", {"username": USERNAME, "password": PASSWORD}, 200),
        ("valid user + wrong pass", {"username": USERNAME, "password": "wrong"}, 401),
        ("unknown user + valid pass", {"username": "ghost", "password": PASSWORD}, 401),
        ("empty user + valid pass", {"username": "", "password": PASSWORD}, 400),
        ("valid user + empty pass", {"username": USERNAME, "password": ""}, 400),
    ]

    status, body = post_json("login", {"username": USERNAME, "password": PASSWORD})
    token = body.get("data", {}).get("refresh_token") if status == 200 else ""

    refresh_combos = [
        ("valid token", {"refresh_token": token}, 200),
        ("missing token", {}, 400),
        ("empty token", {"refresh_token": ""}, 400),
        ("random token", {"refresh_token": "random"}, 401),
    ]

    run_cases("LOGIN COMBINATIONS", "login", login_combos)
    print()
    run_cases("REFRESH COMBINATIONS", "token/refresh", refresh_combos)


if __name__ == "__main__":
    main()
