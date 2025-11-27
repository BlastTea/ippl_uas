"""Execute equivalence-class tests using existing login/refresh helpers."""

from __future__ import annotations

from typing import Callable, List, Tuple

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


TestList = List[Tuple[str, Callable[[], None]]]


def run_login_equivalence() -> None:
    print("=== LOGIN EQUIVALENCE CLASSES ===")
    tests: TestList = [
        ("L1 - Valid credentials", testLoginSuccess),
        ("L2 - Wrong password", testLoginInvalidPass),
        ("L3 - Unknown username", testLoginInvalidUser),
        ("L4 - Missing credentials", testLoginInvalidBody),
        ("L5 - Invalid data types", testLoginInvalidType),
        ("Extra - Wrong user & password combo", testLoginInvalidUserAndPass),
    ]

    for label, func in tests:
        print(f"[{label}]")
        func()
        print()


def run_refresh_equivalence() -> None:
    print("=== REFRESH EQUIVALENCE CLASSES ===")
    tests: TestList = [
        ("R1 - Valid refresh token", testRefreshSuccess),
        ("R2 - Missing refresh token", testRefreshInvalidBody),
        ("R3 - Unknown refresh token", testRefreshInvalid),
        ("R4 - Reused/expired refresh token", testRefreshReuse),
        ("Extra - Protected resource using current access token", testRefreshProtected),
    ]

    for label, func in tests:
        print(f"[{label}]")
        func()
        print()


def main() -> None:
    run_login_equivalence()
    print()
    run_refresh_equivalence()


if __name__ == "__main__":
    main()
