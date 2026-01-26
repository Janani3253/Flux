import os
import json
from phase2_excel_to_web.pages.login_page import LoginPage
from phase2_excel_to_web.utils.credential_loader import get_password


def read_login_data():
    """
    Read login task data passed from run_oem_match via environment variable.
    """
    json_path = os.environ.get("LOGIN_TASKS_FILE")

    if not json_path:
        raise RuntimeError("LOGIN_TASKS_FILE environment variable not set")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Login task file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_oem_login(page):
    rows = read_login_data()

    for row in rows:
        oem = row.get("matched_oem")
        username = row.get("username")
        url = row.get("URL")

        # basic validation
        if not oem or not username or not url:
            print("⏭Skipping row due to missing OEM / username / URL")
            continue

        password = get_password(username)
        if not password:
            print(f" Password missing for username: {username}")
            continue

        print(f" Logging into {oem} as {username}")

        login_page = LoginPage(page)
        login_page.open(url)
        login_page.login(username, password)

        # wait to visually confirm login
        page.wait_for_timeout(5000)
