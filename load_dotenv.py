import os
from pathlib import Path
from typing import Optional, Tuple

_ENV_LOADED = False


def load_dotenv() -> None:
    """Populate os.environ from the nearest .env file (runs once)."""

    global _ENV_LOADED
    if _ENV_LOADED:
        return

    env_path = _find_env_file()
    if not env_path:
        _ENV_LOADED = True
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(raw_line)
        if not parsed:
            continue
        key, value = parsed
        os.environ.setdefault(key, value)

    _ENV_LOADED = True


def _find_env_file() -> Optional[Path]:
    """Search upward from the current working dir and this file for .env."""

    seen: set[Path] = set()
    search_roots = [Path.cwd(), Path(__file__).resolve().parent]

    for root in search_roots:
        current = root
        while True:
            if current in seen:
                break
            seen.add(current)

            candidate = current / ".env"
            if candidate.exists():
                return candidate

            if current.parent == current:
                break
            current = current.parent

    return None


def _parse_env_line(line: str) -> Optional[Tuple[str, str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    if stripped.lower().startswith("export "):
        stripped = stripped[7:]

    if "=" not in stripped:
        return None

    key, _, raw_value = stripped.partition("=")
    key = key.strip()
    if not key:
        return None

    value = _strip_inline_comment(raw_value)
    value = _unquote(value.strip())
    return key, value


def _strip_inline_comment(value: str) -> str:
    result: list[str] = []
    in_single = False
    in_double = False

    for char in value:
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            break
        result.append(char)

    return "".join(result)


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        inner = value[1:-1]
        if value[0] == '"':
            try:
                return bytes(inner, "utf-8").decode("unicode_escape")
            except UnicodeDecodeError:
                return inner
        return inner
    return value
