from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import os
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class SalesInvoicePage:
    def __init__(self, page: Page):
        self.page = page
        self.sales_invoice_path = "/desk/sales-invoice"
        self.add_button = "button:has-text('Add Sales Invoice')"
        self.customer_input = ".form-layout:visible input[data-fieldname='customer']:visible"
        self.edit_item_btn="div[data-original-title='Edit']"
        self.item_code_input = "input[data-fieldname='item_code']"
        self.item_name_input = "textarea[data-fieldname='item_name'], input[data-fieldname='item_name']"
        self.rate_input = "input[data-fieldname='rate']"
        self.qty_input = "input[data-fieldname='qty'], input[data-fieldname='quantity']"
        self.save_button = "button:has-text('Save')"
        self.posting_date_input = "input[data-fieldname='posting_date']"
        self.due_date_input = "input[data-fieldname='due_date']"


    def open_sales_invoice(self):
        try:
            base = self.page.url.split("/desk")[0]
            full_url = f"{base}{self.sales_invoice_path}"
            print(f"Opening Sales Invoice page: {full_url}")
            self.page.goto(full_url, timeout=60000)
            self.page.wait_for_url("**/desk/sales-invoice", timeout=30000)
            self.page.wait_for_selector(self.add_button, timeout=30000)
            print(" Sales Invoice page loaded successfully")
        except PlaywrightTimeoutError:
            raise RuntimeError(" Sales Invoice page did not load properly")

    def click_add_sales_invoice(self):
        print(" Clicking Add Sales Invoice")
        self.page.click(self.add_button)
        # Wait for the form container to actually be visible before proceeding
        self.page.wait_for_selector(".form-layout", state="visible", timeout=10000)


   # Change this part in sales_invoice_page.py
    def fill_invoice_form(self, buyer_name, item_code, item_description, quantity, rate):

        # 1. Handle Customer
        print(f" Searching for Customer: {buyer_name}")
        self.page.wait_for_selector(self.customer_input, state="visible")
        
        # Click and clear to ensure a fresh start
        self.page.click(self.customer_input)
        self.page.fill(self.customer_input, "") 
        
        # Type the name fully WITHOUT interruption
        self.page.type(self.customer_input, buyer_name, delay=150)
        
        # WAIT for the dropdown to appear BEFORE clicking anything else
        suggestion_selector = f"ul.awesomplete li:has-text('{buyer_name}')"
        
        try:
            # Increase timeout slightly to 7 seconds for slower ERP responses
            self.page.wait_for_selector(suggestion_selector, timeout=7000)
            self.page.click(suggestion_selector)
            print(f" Successfully selected {buyer_name} from dropdown")
        except:
            print(f" Dropdown for {buyer_name} didn't appear, trying Enter key...")
            self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(3500) 

        # 2. Open Item Edit Tab/Modal
        print(" Clicking Grid Edit Button")
        self.page.wait_for_selector(self.edit_item_btn, state="visible")
        self.page.click(self.edit_item_btn)

        # 3. Fill Details in the Item section
        print(f" Filling Item Code: {item_code}")
        self.page.wait_for_selector(self.item_code_input, state="visible")
        self.page.fill(self.item_code_input, str(item_code))
        self.page.keyboard.press("Tab") 

        # CRITICAL: Allow ERP to fetch default price/quantity/taxes
        print(" Waiting for ERP background fetch...")
        self.page.wait_for_timeout(1500) 

        # 5. Overwrite with YOUR values
        print(f" Filling Item Name: {item_description}")
        self.page.fill(self.item_name_input, item_description)

        print(f" Forcing Quantity: {quantity}")
        self.page.fill(self.qty_input, "") 
        self.page.fill(self.qty_input, str(quantity))

        print(f" Forcing Rate: {rate}")
        self.page.fill(self.rate_input, "") # Clear ERP default price
        self.page.fill(self.rate_input, str(rate))

        # Finalize
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        print(" Item details finalized")
        print(" Item details filled and modal closed")


    def upload_invoice_pdf(self, invoice_number: str):
        print(" Opening Attachments panel")

        # 1️ Ensure sidebar is visible
        self.page.wait_for_selector(
            ".layout-side-section.right",
            timeout=20000
        )

        # 2️ Click the (+) Attachments button
        self.page.locator(
            "button.add-attachment-btn"
        ).click()

        print(" Attachments dialog opened")

        # 3️ Wait for upload modal
        self.page.wait_for_selector(
            ".modal-dialog",
            timeout=15000
        )

        # 4️ Resolve PDF path (smart search)
        possible_paths = [
            f"data/invoices/{invoice_number}.pdf",
            f"data/input/{invoice_number}.pdf",
            f"data/output/{invoice_number}.pdf",
        ]

        pdf_path = None
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                pdf_path = abs_path
                break

        if not pdf_path:
            raise FileNotFoundError(
                f"PDF not found for invoice {invoice_number}"
            )

        print(f" Uploading PDF: {pdf_path}")

        # 5️ IMPORTANT: Do NOT wait for visibility
        file_input = self.page.locator(
            ".modal-dialog input[type='file']"
        )

        # Just attach the file
        file_input.set_input_files(pdf_path)

        # 6️ Click Upload button
        self.page.locator(
            ".modal-dialog button:has-text('Upload')"
        ).click()

        # 7️ Wait for upload to finish
        self.page.wait_for_timeout(4000)

        print(" PDF uploaded successfully")




    def save_invoice(self):
        print(" Clicking Save button")

        # Give ERP time to finish calculations & background scripts
        self.page.wait_for_timeout(2000)

        save_btn = self.page.locator(
            "#page-Sales\\ Invoice .standard-actions button:has-text('Save')"
        )

        # Wait for the REAL visible Save button
        save_btn.wait_for(state="visible", timeout=20000)

        # Click Save
        save_btn.click()

    # Wait for ERP save to complete
        self.page.wait_for_timeout(6000)

        print(" Invoice saved successfully")


