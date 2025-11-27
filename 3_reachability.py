"""Reachability testing driver referencing PPT concept."""

from __future__ import annotations

from collections import deque
from typing import Callable, Dict, Iterable, List

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

StateHandler = Callable[[], None]


def _log_state(state: str) -> None:
    print(f"\n=== STATE: {state} ===")


ACTIONS: Dict[str, StateHandler] = {
    "START": lambda: print("Mulai pengujian keterjangkauan"),
    "LOGIN_SUCCESS": testLoginSuccess,
    "LOGIN_INVALID_USER": testLoginInvalidUser,
    "LOGIN_INVALID_PASS": testLoginInvalidPass,
    "LOGIN_INVALID_BODY": testLoginInvalidBody,
    "LOGIN_INVALID_TYPE": testLoginInvalidType,
    "LOGIN_INVALID_USERPASS": testLoginInvalidUserAndPass,
    "REFRESH_PROTECTED": testRefreshProtected,
    "REFRESH_SUCCESS": testRefreshSuccess,
    "REFRESH_INVALID_BODY": testRefreshInvalidBody,
    "REFRESH_INVALID": testRefreshInvalid,
    "REFRESH_REUSE": testRefreshReuse,
}

GRAPH: Dict[str, List[str]] = {
    "START": [
        "LOGIN_SUCCESS",
        "LOGIN_INVALID_USER",
        "LOGIN_INVALID_PASS",
        "LOGIN_INVALID_BODY",
        "LOGIN_INVALID_TYPE",
        "LOGIN_INVALID_USERPASS",
    ],
    "LOGIN_SUCCESS": [
        "REFRESH_PROTECTED",
        "REFRESH_SUCCESS"
    ],
    "REFRESH_SUCCESS": [
        "REFRESH_INVALID_BODY",
        "REFRESH_INVALID",
        "REFRESH_REUSE"
    ],
}


def traverse(start: str = "START") -> Iterable[str]:
    visited: set[str] = set()
    queue: deque[str] = deque([start])

    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)

        _log_state(state)
        handler = ACTIONS.get(state)
        if handler:
            handler()
        else:
            print("Tidak ada aksi untuk state ini.")

        for neighbor in GRAPH.get(state, []):
            queue.append(neighbor)

    return visited


def main() -> None:
    visited = set(traverse())
    missing = set(ACTIONS) - visited

    print("\n=== RINGKASAN ===")
    print(f"State tercapai : {len(visited)} / {len(ACTIONS)}")
    if missing:
        print("State yang belum tercapai:", ", ".join(sorted(missing)))
    else:
        print("Seluruh state tercapai.")


if __name__ == "__main__":
    main()
