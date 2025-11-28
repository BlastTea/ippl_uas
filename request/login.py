"""Login helper that wraps the backend login endpoint."""

from __future__ import annotations

import os

from load_dotenv import load_dotenv

from typing import Any, Dict, Tuple

from .http_client import post_json

ACCESS_TOKEN = None
REFRESH_TOKEN = None


def login(username: str, password: str) -> Tuple[int, Dict[str, Any]]:
    """Send login request and return (status_code, response_dict)."""

    payload = {"username": username, "password": password}
    return post_json("login", payload)

def testLoginSuccess():
    global ACCESS_TOKEN
    global REFRESH_TOKEN

    ACCESS_TOKEN = None
    REFRESH_TOKEN = None

    load_dotenv()

    status, body = login(os.getenv("USERNAME_LOGIN"), os.getenv("PASSWORD_LOGIN"))

    if status == 200 and "data" in body:
        data = body["data"]
        token_type = data.get("token_type")
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")
        username = data.get("user", {}).get("username")
        
        if (
            token_type == "Bearer"
            and access_token
            and refresh_token
            and username == os.getenv("USERNAME_LOGIN")
        ):
            ACCESS_TOKEN = access_token
            REFRESH_TOKEN = refresh_token
            
            print("TC-LOGIN-001, Success")
            return
        
        if token_type != "Bearer":
            print("TC-LOGIN-001, Failed : token_type is not Bearer")
            return
        if ACCESS_TOKEN is None:
            print("TC-LOGIN-001, Failed : access_token is null")
            return
        if REFRESH_TOKEN is None:
            print("TC-LOGIN-001, Failed : refresh_token is null")
            return

    print("TC-LOGIN-001, Failed : ", body.get("error", "Unknown error"))

def testLoginInvalidUserAndPass():
    status, body = login("Hello", "World")

    if status == 401:
        print("TC-LOGIN-002, Success")
        return
    
    print("TC-LOGIN-002, Failed : ", body.get("error", "Unknown error"))

def testLoginInvalidUser():
    load_dotenv()

    status, body = login("Hello", os.getenv("PASSWORD_LOGIN"))

    if status == 401:
        print("TC-LOGIN-003, Success")
        return
    
    print("TC-LOGIN-003, Failed : ", body.get("error", "Unknown error"))

def testLoginInvalidPass():
    load_dotenv()

    status, body = login(os.getenv("USERNAME_LOGIN"), "World")

    if status == 401:
        print("TC-LOGIN-004, Success")
        return
    
    print("TC-LOGIN-004, Failed : ", body.get("error", "Unknown error"))

def testLoginInvalidBody():
    status, body = post_json("login", {})

    if status == 400:
        print("TC-LOGIN-005, Success")
        return

    print("TC-LOGIN-005, Failed : ", body.get("error", "Unknown error"))


def testLoginInvalidType():
    payload = {"username": 123, "password": False}  # type: ignore[dict-item]
    status, body = post_json("login", payload)

    if status == 400:
        print("TC-LOGIN-006, Success")
        return

    print("TC-LOGIN-006, Failed : ", body.get("error", "Unknown error"))
