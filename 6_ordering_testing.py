"""Ordering testing"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from load_dotenv import load_dotenv
from request.http_client import get_json
from request import login as login_module

load_dotenv()


def ensure_logged_in() -> str:
    if login_module.ACCESS_TOKEN and login_module.REFRESH_TOKEN:
        return login_module.ACCESS_TOKEN

    login_module.testLoginSuccess()
    token = login_module.ACCESS_TOKEN
    if not token:
        raise RuntimeError("Failed to obtain access token for ordering test.")
    return token


def fetch_surveys(access_token: str) -> Tuple[int, Dict[str, Any]]:
    return get_json(
        "surveys/customer",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def is_sorted(values: List[int]) -> bool:
    return values == sorted(values)


def run_ordering_test() -> None:
    token = ensure_logged_in()
    status, body = fetch_surveys(token)

    if status != 200:
        print("Ordering test FAILED: HTTP", status, "|", body.get("error"))
        return

    surveys = body.get("data")
    if not isinstance(surveys, list):
        print("Ordering test FAILED: unexpected surveys payload")
        return

    ids = [entry.get("id") for entry in surveys if isinstance(entry, dict) and entry.get("id") is not None]

    if not ids:
        print("Ordering test WARNING: no survey data to verify")
        return

    if is_sorted(ids):
        print("Ordering test PASS: survey IDs are sorted ascending.")
    else:
        print("Ordering test FAIL: survey IDs unordered.", ids)


def main() -> None:
    run_ordering_test()


if __name__ == "__main__":
    main()
