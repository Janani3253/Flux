from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


class SalesInvoicePage:
    def __init__(self, page: Page):
        self.page = page
        self.sales_invoice_path = "/desk/sales-invoice"

        # MUCH more stable selector
        self.add_button = "button:has-text('Add Sales Invoice')"

    def open_sales_invoice(self):
        try:
            base = self.page.url.split("/desk")[0]
            full_url = f"{base}{self.sales_invoice_path}"

            print(f"Opening Sales Invoice page: {full_url}")
            self.page.goto(full_url, timeout=60000)

            #  Validate by URL (SPA-safe)
            self.page.wait_for_url("**/desk/sales-invoice", timeout=30000)

            #  Validate by button (real user action)
            self.page.wait_for_selector(self.add_button, timeout=30000)

            print(" Sales Invoice page loaded successfully")

        except PlaywrightTimeoutError:
            raise RuntimeError(" Sales Invoice page did not load properly")

    def click_add_sales_invoice(self):
        print(" Clicking Add Sales Invoice")
        self.page.click(self.add_button)
