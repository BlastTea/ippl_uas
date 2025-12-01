from __future__ import annotations


def hitung_diskon(total: float) -> float:
    diskon = 0.0
    if total >= 500_000:
        diskon = 0.2
    elif total >= 200_000:
        diskon = 0.1
    else:
        diskon = 0.05
    return total - (total * diskon)


def main() -> None:
    test_cases = [
        {"desc": "DU1 - total >= 500000", "total": 600_000, "expected": 480_000},
        {"desc": "DU2 - 200000 <= total < 500000", "total": 300_000, "expected": 270_000},
        {"desc": "DU3 - total < 200000", "total": 150_000, "expected": 142_500},
    ]

    print("=== Data Flow Testing: hitung_diskon() ===")
    for tc in test_cases:
        hasil = hitung_diskon(tc["total"])
        status = "OK" if hasil == tc["expected"] else "FAIL"
        print(
            f"{tc['desc']:35} | Total: Rp{tc['total']:,} "
            f"| Hasil: Rp{hasil:,.0f} | Expected: Rp{tc['expected']:,.0f} | {status}"
        )


if __name__ == "__main__":
    main()

