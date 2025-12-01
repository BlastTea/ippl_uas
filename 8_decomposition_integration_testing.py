from __future__ import annotations

import os

from load_dotenv import load_dotenv
from request.http_client import get_json
from request.login import login
from request.refresh import refresh


def login_and_protected() -> bool:
    username = os.getenv("USERNAME_LOGIN")
    password = os.getenv("PASSWORD_LOGIN")
    if not username or not password:
        print("DI-001 Login + Protected: FAIL (missing credentials in .env)")
        return False

    status, body = login(username, password)
    if status != 200 or "data" not in body:
        print("DI-001 Login + Protected: FAIL (login)", status, body.get("error"))
        return False

    access_token = body["data"].get("access_token")
    if not access_token:
        print("DI-001 Login + Protected: FAIL (no access_token)")
        return False

    status2, body2 = get_json("surveys/customer", headers={"Authorization": f"Bearer {access_token}"})
    if status2 == 200:
        print("DI-001 Login + Protected: PASS")
        return True

    print("DI-001 Login + Protected: FAIL (protected)", status2, body2.get("error"))
    return False


def login_refresh_protected() -> bool:
    username = os.getenv("USERNAME_LOGIN")
    password = os.getenv("PASSWORD_LOGIN")
    if not username or not password:
        print("DI-002 Login + Refresh + Protected: FAIL (missing credentials in .env)")
        return False

    status, body = login(username, password)
    if status != 200 or "data" not in body:
        print("DI-002 Login + Refresh + Protected: FAIL (login)", status, body.get("error"))
        return False

    refresh_token = body["data"].get("refresh_token")
    if not refresh_token:
        print("DI-002 Login + Refresh + Protected: FAIL (no refresh_token)")
        return False

    status2, body2 = refresh(refresh_token)
    if status2 != 200 or "data" not in body2:
        print("DI-002 Login + Refresh + Protected: FAIL (refresh)", status2, body2.get("error"))
        return False

    new_access = body2["data"].get("access_token")
    if not new_access:
        print("DI-002 Login + Refresh + Protected: FAIL (no new access_token)")
        return False

    status3, body3 = get_json("surveys/customer", headers={"Authorization": f"Bearer {new_access}"})
    if status3 == 200:
        print("DI-002 Login + Refresh + Protected: PASS")
        return True

    print("DI-002 Login + Refresh + Protected: FAIL (protected)", status3, body3.get("error"))
    return False


def main() -> None:
    load_dotenv()
    login_and_protected()
    login_refresh_protected()


if __name__ == "__main__":
    main()

