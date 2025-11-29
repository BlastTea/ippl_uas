"""Ordering check for /surveys/customer."""

from request import login as login_module
from request.http_client import get_json


def main() -> None:
    login_module.testLoginSuccess()
    token = login_module.ACCESS_TOKEN

    status, body = get_json("surveys/customer", headers={"Authorization": f"Bearer {token}"})
    if status != 200 or not isinstance(body.get("data"), list):
        print("Ordering test FAILED:", status, body.get("error"))
        return

    ids = [item.get("id") for item in body["data"] if isinstance(item, dict)]
    if ids == sorted(ids):
        print("Ordering test PASS: IDs sorted ascending")
    else:
        print("Ordering test FAIL: IDs not sorted", ids)


if __name__ == "__main__":
    main()
