import os
import json
from playwright.sync_api import Page
from phase2_excel_to_web.pages.login_page import LoginPage
from phase2_excel_to_web.pages.sales_invoice_page import SalesInvoicePage
from phase2_excel_to_web.utils.credential_loader import get_password

def read_login_data():
    """
    Read login task data passed from the JSON file stored in the temp folder
    via the LOGIN_TASKS_FILE environment variable.
    """
    json_path = os.environ.get("LOGIN_TASKS_FILE")
    
    if not json_path:
        raise RuntimeError("LOGIN_TASKS_FILE environment variable not set")
    
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Login task file not found at: {json_path}")
        
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
    # Load all rows from the JSON stored in the temp folder
    rows = read_login_data()

    for index, row in enumerate(rows, start=1):
        # 1. Extraction from JSON (Mapping to your specific keys)
        oem = row.get("matched_oem")
        username = row.get("username")
        url = row.get("URL")
        
        # Form filling data
        buyer_name = row.get("Buyer Name")
        item_code = row.get("Item Code")
        item_desc = row.get("OEM / Description")
        total_amt = row.get("Total Invoice Amount")

        print(f"\n--- Processing Row {index} ---")

        # 2. Basic validation
        if not oem or not username or not url:
            print(f" Skipping row {index} due to missing URL/Credentials")
            continue

        # Fetch password using the utility
        password = get_password(username)
        if not password:
            print(f" Skipping: No password found for {username}")
            continue

        target_url = normalize_url(url)

        print(f" Logging into {oem} as {username}")
        print(f" Target Site: {target_url}")

        # 3. Execution - LOGIN
        login_page = LoginPage(page)
        login_page.open(target_url)
        login_page.login(username, password)

        # 4. Execution - NAVIGATION
        sales_page = SalesInvoicePage(page)
        sales_page.open_sales_invoice()
        sales_page.click_add_sales_invoice()

        # 5. Execution - FORM FILLING
        # This calls the method in your SalesInvoicePage class
        if buyer_name:
            print(f" Filling form for Buyer: {buyer_name}")
            sales_page.fill_invoice_form(
                buyer_name=buyer_name,
                item_code=item_code,
                item_description=oem,
                total_amount=total_amt
            )

        print(f" Finished processing {buyer_name} for OEM {oem}")
        
        # Brief pause to verify results before next row
        
        page.wait_for_timeout(15000)