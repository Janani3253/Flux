from playwright.sync_api import Page
from phase2_excel_to_web.pages.login_page import LoginPage
from phase2_excel_to_web.pages.sales_invoice_page import SalesInvoicePage
from phase2_excel_to_web.utils.credential_loader import get_password
from phase2_excel_to_web.shared.runtime_store import RUNTIME_DATA


def normalize_url(url: str) -> str:
    """
    Ensure URL has protocol (https://).
    """
    url_str = str(url).strip()
    if not url_str.startswith(("http://", "https://")):
        return f"https://{url_str}"
    return url_str


def test_oem_login(page: Page):
    """
    Playwright test driven entirely from in-memory runtime data (NO JSON).
    """

    rows = RUNTIME_DATA.get("invoices", [])

    if not rows:
        raise RuntimeError("No invoice data found in RUNTIME_DATA")

    for index, row in enumerate(rows, start=1):
        print(f"\n--- Processing Row {index} ---")

        try:
            # ---------------- EXTRACT DATA ----------------
            username = row.get("username")
            oem = row.get("matched_oem")
            OEM = row.get("OEM")

            url = row.get("URL")
            buyer_name = row.get("Buyer Name")

            item_code = row.get("Item Code")
            item_desc = row.get("OEM / Description")
            quantity = row.get("Quantity")
            rate = row.get("Rate")

            invoice_number = row.get("Invoice Number") or row.get("invoiceNumber")

            # ---------------- VALIDATION ----------------
            if not username or not url or not buyer_name:
                raise ValueError("Missing username / url / buyer name")

            if item_code is None or item_desc is None or quantity is None or rate is None:
                raise ValueError("Missing item data")

            quantity = int(quantity)
            rate = float(rate)

            # ---------------- LOGIN ----------------
            password = get_password(OEM)
            if not password:
                raise RuntimeError(f"No password found for OEM: {OEM}")

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

            # ---------------- SAVE ----------------
            sales_page.save_invoice()

            # ---------------- UPLOAD PDF ----------------
            if invoice_number:
                sales_page.upload_invoice_pdf(invoice_number)

            # ---------------- SUCCESS ----------------
            row["Status"] = "SUCCESS"
            row["Error"] = ""

            print(f" ✔ SUCCESS for {buyer_name} ({oem})")

        except Exception as exc:
            # ---------------- FAILURE HANDLING ----------------
            row["Status"] = "FAILED"
            row["Error"] = str(exc)

            print(f" ✖ FAILED for Row {index}: {exc}")

        finally:
            # Small pause between rows (ERP safety)
            page.wait_for_timeout(3000)
