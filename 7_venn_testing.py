"""Venn-style testing script for login & refresh"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from load_dotenv import load_dotenv
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

load_dotenv()


Action = Callable[[], None]


@dataclass
class VennScenario:
    label: str
    description: str
    sets: Dict[str, bool]
    action: Action


def _print_sets(sets: Dict[str, bool]) -> None:
    included = [name for name, value in sets.items() if value]
    excluded = [name for name, value in sets.items() if not value]
    print(f"    In : {', '.join(included) or '-'}")
    print(f"    Out: {', '.join(excluded) or '-'}")


def run_login_venn() -> None:
    print("=== LOGIN VENN SCENARIOS ===")

    scenarios: List[VennScenario] = [
        VennScenario(
            label="L-A&B",
            description="Username valid AND password valid",
            sets={"Username matches existing user": True, "Password matches stored hash": True},
            action=testLoginSuccess,
        ),
        VennScenario(
            label="L-A&~B",
            description="Username valid BUT password wrong",
            sets={"Username matches existing user": True, "Password matches stored hash": False},
            action=testLoginInvalidPass,
        ),
        VennScenario(
            label="L-~A&B",
            description="Username missing/unknown BUT password valid",
            sets={"Username matches existing user": False, "Password matches stored hash": True},
            action=testLoginInvalidUser,
        ),
        VennScenario(
            label="L-~A&~B",
            description="Username & password both invalid",
            sets={"Username matches existing user": False, "Password matches stored hash": False},
            action=testLoginInvalidUserAndPass,
        ),
        VennScenario(
            label="L-Empty",
            description="Credentials absent (outside both sets)",
            sets={"Username matches existing user": False, "Password matches stored hash": False},
            action=testLoginInvalidBody,
        ),
    ]

    for scenario in scenarios:
        print(f"[{scenario.label}] {scenario.description}")
        _print_sets(scenario.sets)
        scenario.action()
        print()


def run_refresh_venn() -> None:
    print("=== REFRESH VENN SCENARIOS ===")

    # Reset tokens before refresh section.
    testLoginSuccess()

    scenarios: List[VennScenario] = [
        VennScenario(
            label="R-Issued&Fresh",
            description="Token issued by backend AND not yet used",
            sets={"Token issued": True, "Token fresh": True},
            action=testRefreshSuccess,
        ),
        VennScenario(
            label="R-Issued&~Fresh",
            description="Token issued but already used/revoked",
            sets={"Token issued": True, "Token fresh": False},
            action=testRefreshReuse,
        ),
        VennScenario(
            label="R-~Issued&Provided",
            description="Token supplied but never issued",
            sets={"Token issued": False, "Token fresh": False},
            action=testRefreshInvalid,
        ),
        VennScenario(
            label="R-~Issued&~Provided",
            description="Token missing entirely",
            sets={"Token issued": False, "Token fresh": False},
            action=testRefreshInvalidBody,
        ),
    ]

    for scenario in scenarios:
        print(f"[{scenario.label}] {scenario.description}")
        _print_sets(scenario.sets)
        scenario.action()
        print()


def main() -> None:
    run_login_venn()
    run_refresh_venn()


if __name__ == "__main__":
    main()
