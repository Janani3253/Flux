from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

class SalesInvoicePage:
    def __init__(self, page: Page):
        self.page = page
        self.sales_invoice_path = "/desk/sales-invoice"

        self.add_button = "button:has-text('Add Sales Invoice')"
        
        # IMPROVED SELECTOR: Added :visible to ensure we only target the active field
        # and added a parent container to avoid the "2 elements found" conflict
        self.customer_input = ".form-layout:visible input[data-fieldname='customer']:visible"
        
        self.edit_item_btn = "#sales-invoice-__details > div:nth-child(6) > div > div > form > div > div > div.form-grid-container.column-limit-reached > div > div.grid-body > div.rows > div > div.data-row.row.m-0 > div:nth-child(8) > div > a"
        
        self.item_code_input = "input[data-fieldname='item_code']"
        self.item_name_input = "textarea[data-fieldname='item_name'], input[data-fieldname='item_name']"
        self.rate_input = "input[data-fieldname='rate']"
        
        self.save_button = "button:has-text('Save')"

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
    def fill_invoice_form(self, buyer_name, item_code, item_description, total_amount):
        # 1. Handle Customer
        # S.DEEPANKUMAR -> DEEPANKUMAR
        clean_name = buyer_name.split('.')[-1].strip()
        # Use a short part of the name to trigger the search
        search_term = clean_name[:5] 

        print(f" Searching for Customer: {search_term}")
        self.page.wait_for_selector(self.customer_input, state="visible")
        self.page.click(self.customer_input)
        self.page.fill(self.customer_input, "") 
        self.page.type(self.customer_input, search_term, delay=150)
        
        # NEW STRATEGY: Wait for the specific list item to appear and click it
        # This prevents selecting the wrong person or "Create New"
        print(f" Waiting for dropdown option containing {clean_name}...")
        suggestion_selector = f"ul.awesomplete li:has-text('{clean_name}')"
        
        try:
            self.page.wait_for_selector(suggestion_selector, timeout=5000)
            self.page.click(suggestion_selector)
            print(f" Selected {clean_name} from dropdown")
        except PlaywrightTimeoutError:
            print(f" Specific suggestion not found, falling back to Enter key")
            self.page.keyboard.press("Enter")

        
        # ERPNext specific: Wait for the search to trigger and dropdown to show
        self.page.wait_for_timeout(2000) 
        
        # Press ArrowDown then Enter to select the first suggestion
        # This is more reliable than clicking a specific text match
        
        self.page.wait_for_timeout(1000)

        # 2. Open Item Edit Tab/Modal
        print(" Clicking Grid Edit Button")
        self.page.wait_for_selector(self.edit_item_btn, state="visible")
        self.page.click(self.edit_item_btn)

        # 3. Fill Details in the Item section
        print(f" Filling Item Code: {item_code}")
        self.page.wait_for_selector(self.item_code_input, state="visible")
        # Clear and fill for safety
        self.page.fill(self.item_code_input, "")
        self.page.fill(self.item_code_input, str(item_code))
        
        print(f" Filling Item Name (OEM): {item_description}")
        self.page.fill(self.item_name_input, "")
        self.page.fill(self.item_name_input, item_description)

        print(f" Filling Rate (Amount): {total_amount}")
        self.page.fill(self.rate_input, "")
        self.page.fill(self.rate_input, str(total_amount))
        
        # Trigger an 'Enter' to make sure the value registers before Escaping
        self.page.keyboard.press("Enter")
        self.page.wait_for_timeout(500)
        self.page.keyboard.press("Escape")
        print(" Item details filled and modal closed")

        # 4. Save Function (Commented out)
        # print(" Clicking Save")
        # self.page.click(self.save_button)