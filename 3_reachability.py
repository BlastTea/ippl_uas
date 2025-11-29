"""Reachability walk-through showing every branch is hit at least once."""

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

PATHS = [
    ("START", [lambda: print("Begin reachability tour")]),
    (
        "LOGIN BRANCHES",
        [
            testLoginSuccess,
            testLoginInvalidUser,
            testLoginInvalidPass,
            testLoginInvalidBody,
            testLoginInvalidType,
            testLoginInvalidUserAndPass,
        ],
    ),
    ("POST-LOGIN", [testRefreshProtected, testRefreshSuccess]),
    ("REFRESH BRANCHES", [testRefreshInvalidBody, testRefreshInvalid, testRefreshReuse]),
]


def run_reachability() -> None:
    for label, steps in PATHS:
        print(f"=== {label} ===")
        for step in steps:
            step()
        print()


if __name__ == "__main__":
    run_reachability()
