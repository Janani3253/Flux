import os
import json
from playwright.sync_api import Page
from phase2_excel_to_web.pages.login_page import LoginPage
from phase2_excel_to_web.pages.sales_invoice_page import SalesInvoicePage
from phase2_excel_to_web.utils.credential_loader import get_password


def read_login_data():
    """
    Read login task data passed from run_oem_match via environment variable.
    """
    json_path = os.environ.get("LOGIN_TASKS_FILE")

    if not json_path:
        raise RuntimeError(" LOGIN_TASKS_FILE environment variable not set")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f" Login task file not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_url(url: str) -> str:
    """
    Ensure URL has protocol (https://).
    """
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url


def test_oem_login(page: Page):
    rows = read_login_data()

    for index, row in enumerate(rows, start=1):
        oem = row.get("matched_oem")
        username = row.get("username")
        url = row.get("URL")

        print(f"\n Processing row {index}")

        # basic validation
        if not oem or not username or not url:
            print(" Skipping row due to missing OEM / username / URL")
            continue

        password = get_password(username)
        if not password:
            print(f" Password missing for username: {username}")
            continue

        url = normalize_url(url)

        print(f" Logging into {oem} as {username}")
        print(f" URL: {url}")

        # ---------- LOGIN ----------
        login_page = LoginPage(page)
        login_page.open(url)
        login_page.login(username, password)

        # ---------- NAVIGATE TO SALES INVOICE ----------
        sales_page = SalesInvoicePage(page)
        sales_page.open_sales_invoice()
        sales_page.click_add_sales_invoice()

        print(f" Successfully reached Add Sales Invoice page for {oem}")

        # Optional visual pause (can remove later)
        page.wait_for_timeout(3000)
