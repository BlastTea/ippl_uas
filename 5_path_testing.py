from __future__ import annotations


def cek_nilai(nilai: int) -> str:
    if nilai >= 80:
        return "A"
    if nilai >= 60:
        return "B"
    return "C"


def cyclomatic_complexity() -> int:
    """CC = P + 1 = 3"""
    return 3


def main() -> None:
    print(f"Cyclomatic Complexity: {cyclomatic_complexity()}")
    cases = [
        ("Path 1 (A branch)", 85, "A"),
        ("Path 2 (B branch)", 70, "B"),
        ("Path 3 (C branch)", 40, "C"),
    ]
    for label, value, expected in cases:
        result = cek_nilai(value)
        status = "PASS" if result == expected else "FAIL"
        print(f"{label}: input={value} expected={expected} got={result} -> {status}")


if __name__ == "__main__":
    main()
