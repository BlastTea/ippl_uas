from __future__ import annotations

from request.login import (
    testLoginInvalidBody,
    testLoginInvalidPass,
    testLoginInvalidType,
    testLoginInvalidUser,
    testLoginInvalidUserAndPass,
    testLoginSuccess,
)
from request.refresh import (
    testRefreshInvalid,
    testRefreshInvalidBody,
    testRefreshProtected,
    testRefreshReuse,
    testRefreshSuccess,
)


def run_all() -> None:
    login_tests = [
        testLoginSuccess,
        testLoginInvalidUserAndPass,
        testLoginInvalidUser,
        testLoginInvalidPass,
        testLoginInvalidBody,
        testLoginInvalidType,
    ]
    refresh_tests = [
        testRefreshSuccess,
        testRefreshInvalid,
        testRefreshProtected,
        testRefreshReuse,
        testRefreshInvalidBody,
    ]

    print("=== AUTOMATIC LOGIN TESTS ===")
    for func in login_tests:
        func()

    print("\n=== AUTOMATIC REFRESH TESTS ===")
    for func in refresh_tests:
        func()


if __name__ == "__main__":
    run_all()

