"""Equivalence-class runner."""

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

LOGIN_CASES = [
    ("L1 valid credentials", testLoginSuccess),
    ("L2 wrong password", testLoginInvalidPass),
    ("L3 unknown username", testLoginInvalidUser),
    ("L4 missing credentials", testLoginInvalidBody),
    ("L5 invalid data types", testLoginInvalidType),
    ("Extra wrong user+pass", testLoginInvalidUserAndPass),
]

REFRESH_CASES = [
    ("R1 valid refresh token", testRefreshSuccess),
    ("R2 missing refresh token", testRefreshInvalidBody),
    ("R3 unknown refresh token", testRefreshInvalid),
    ("R4 reused refresh token", testRefreshReuse),
    ("Extra protected endpoint", testRefreshProtected),
]


def run_equivalence(login: bool = True, refresh: bool = True) -> None:
    if login:
        print("=== LOGIN EQUIVALENCE ===")
        for label, func in LOGIN_CASES:
            print(label)
            func()
            print()

    if refresh:
        print("=== REFRESH EQUIVALENCE ===")
        for label, func in REFRESH_CASES:
            print(label)
            func()
            print()


if __name__ == "__main__":
    run_equivalence()
