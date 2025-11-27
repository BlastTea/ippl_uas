"""Refresh token helper for the sigma backend."""

from __future__ import annotations

import os

from typing import Any, Dict, Tuple

from request import login as login_module

from .http_client import post_json, get_json


def refresh(refresh_token: str) -> Tuple[int, Dict[str, Any]]:
    """Send refresh token request and return (status_code, response_dict)."""

    payload = {"refresh_token": refresh_token}
    return post_json("token/refresh", payload)


def _current_access_token() -> str:
    token = getattr(login_module, "ACCESS_TOKEN", None)
    if not token:
        raise RuntimeError("Access token is missing. Run testLoginSuccess first.")
    return token

def _current_refresh_token() -> str:
    token = getattr(login_module, "REFRESH_TOKEN", None)
    if not token:
        raise RuntimeError("Refresh token is missing. Run testLoginSuccess first.")
    return token

def testRefreshSuccess():
    try:
        refresh_token = _current_refresh_token()
    except RuntimeError as exc:
        print(f"TC-REFRESH-001, Failed : {exc}")
        return

    status, body = refresh(refresh_token)

    if status == 200 and "data" in body:
        data = body["data"]
        token_type = data.get("token_type")
        access_token = data.get("access_token")
        new_refresh = data.get("refresh_token")
        username = data.get("user", {}).get("username")

        if (
            token_type == "Bearer"
            and access_token
            and new_refresh
            and username == os.getenv("USERNAME_LOGIN")
        ):
            login_module.ACCESS_TOKEN = access_token
            login_module.REFRESH_TOKEN = new_refresh

            print("TC-REFRESH-001, Success")
            return

        if token_type != "Bearer":
            print("TC-REFRESH-001, Failed : token_type is not Bearer")
            return
        if not access_token:
            print("TC-REFRESH-001, Failed : access_token is null")
            return
        if not new_refresh:
            print("TC-REFRESH-001, Failed : refresh_token is null")
            return

    print("TC-REFRESH-001, Failed : ", body.get("error", "Unknown error"))

def testRefreshInvalid():
    status, body = refresh("ABC123")
    
    if status == 401:
        print("TC-REFRESH-002, Success")
        return
    
    print("TC-REFRESH-002, Failed : ", body.get("error", "Unknown error"))
    
def testRefreshProtected():
    try:
        access_token = _current_access_token()
    except RuntimeError as exc:
        print(f"TC-REFRESH-003, Failed : {exc}")
        return
    
    status, body = get_json("surveys/customer", headers={"Authorization": f"Bearer {access_token}"})
    
    if status == 200:
        print("TC-REFRESH-003, Success")
        return

    print("TC-REFRESH-003, Failed : ", body.get("error", "Unknown error"))

def testRefreshReuse():
    try:
        refresh_token = _current_refresh_token()
    except RuntimeError as exc:
        print(f"TC-REFRESH-004, Failed : {exc}")
        return

    refresh(refresh_token)
    status, body = refresh(refresh_token)
    
    if status == 401:
        print("TC-REFRESH-004, Success")
        return

    print("TC-REFRESH-004, Failed : ", body.get("error", "Unknown error"))