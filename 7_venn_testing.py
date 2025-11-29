"""Quick Venn-style coverage report."""

from request.login import (
    testLoginInvalidBody,
    testLoginInvalidPass,
    testLoginInvalidUser,
    testLoginInvalidUserAndPass,
    testLoginSuccess,
)
from request.refresh import (
    testRefreshInvalid,
    testRefreshInvalidBody,
    testRefreshReuse,
    testRefreshSuccess,
)


def show(title: str, tests: list[tuple[str, callable]]) -> None:
    print(f"=== {title} ===")
    for label, func in tests:
        print(label)
        func()
        print()


def main() -> None:
    login_sets = [
        ("Username+Password valid", testLoginSuccess),
        ("Username valid, Password invalid", testLoginInvalidPass),
        ("Username invalid, Password valid", testLoginInvalidUser),
        ("Username invalid, Password invalid", testLoginInvalidUserAndPass),
        ("Credentials missing", testLoginInvalidBody),
    ]

    refresh_sets = [
        ("Token issued & fresh", testRefreshSuccess),
        ("Token issued & reused", testRefreshReuse),
        ("Token never issued", testRefreshInvalid),
        ("Token missing", testRefreshInvalidBody),
    ]

    show("LOGIN SETS", login_sets)
    show("REFRESH SETS", refresh_sets)


if __name__ == "__main__":
    main()
