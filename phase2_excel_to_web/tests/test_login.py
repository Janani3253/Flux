import os
import json
from playwright.sync_api import Page
from phase2_excel_to_web.pages.login_page import LoginPage
from phase2_excel_to_web.pages.sales_invoice_page import SalesInvoicePage
from phase2_excel_to_web.utils.credential_loader import get_password


def read_login_data():
    """
    Read Playwright task data from the JSON file stored in the temp folder
    via the PLAYWRIGHT_TASKS_FILE environment variable.
    """
    json_path = os.environ.get("PLAYWRIGHT_TASKS_FILE")

    if not json_path:
        raise RuntimeError("PLAYWRIGHT_TASKS_FILE environment variable not set")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Playwright task file not found at: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_url(url: str) -> str:
    """
    Ensure URL has protocol (https://).
    """
    url_str = str(url).strip()
    if not url_str.startswith(("http://", "https://")):
        return f"https://{url_str}"
    return url_str


def test_oem_login(page: Page):
    rows = read_login_data()

    for index, row in enumerate(rows, start=1):
        print(f"\n--- Processing Row {index} ---")

        # ---------------- EXTRACT DATA (FLAT JSON) ----------------
        username = row.get("username")
        oem = row.get("matched_oem")
        OEM=row.get("OEM")

        url = row.get("URL")
        buyer_name = row.get("Buyer Name")

        item_code = row.get("Item Code")
        item_desc = row.get("OEM / Description")
        quantity = row.get("quantity")
        rate = row.get("rate")

        # ---------------- VALIDATION ----------------
        if not username or not url or not buyer_name:
            print(" Skipping row: missing username/url/customer_name")
            continue

        if item_code is None or item_desc is None or quantity is None or rate is None:
            print(" Skipping row: missing item data")
            continue

        # Ensure correct data types
        try:
            quantity = int(quantity)
            rate = float(rate)
        except ValueError:
            print(" Skipping row: invalid quantity or rate")
            continue

        # ---------------- LOGIN ----------------
        password = get_password(OEM)
        if not password:
            print(f" Skipping: No password found for {username}")
            continue

        target_url = normalize_url(url)

        print(f" Logging into {oem} as {username}")
        print(f" Target Site: {target_url}")

        login_page = LoginPage(page)
        login_page.open(target_url)
        login_page.login(username, password)

        # ---------------- NAVIGATION ----------------
        sales_page = SalesInvoicePage(page)
        sales_page.open_sales_invoice()
        sales_page.click_add_sales_invoice()

        # ---------------- FORM FILLING ----------------
        print(f" Filling form for Buyer: {buyer_name}")

        sales_page.fill_invoice_form(
            buyer_name=buyer_name,
            item_code=item_code,
            item_description=item_desc,
            quantity=quantity,
            rate=rate
        )
                # ---------------- SAVE INVOICE ----------------
        sales_page.save_invoice()

        print(f" Finished processing {buyer_name} for OEM {oem}")
        page.wait_for_timeout(3000)
        # Upload PDF using invoice number
        invoice_number = row.get("invoiceNumber")  # SALE-CR-2573
        sales_page.upload_invoice_pdf(invoice_number)

        # Pause to visually confirm result before next iteration
        page.wait_for_timeout(30000)
