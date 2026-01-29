from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = "input[name='username'], input[type='text']"
        self.password_input = "input[name='password'], input[type='password']"
        self.login_button = "button[type='submit'], input[type='submit']"

        # ERPNext permission popup selectors
        self.permission_popup = "text=Not permitted"
        self.popup_close_btn = "button[aria-label='Close'], .modal-close"

    def open(self, url: str):
        print(f" Opening URL: {url}")
        self.page.goto(url, timeout=60000, wait_until="load")

    def login(self, username: str, password: str):
        print(" Waiting for username field...")
        self.page.wait_for_selector(self.username_input, timeout=30000)

        print(" Entering username")
        self.page.fill(self.username_input, username)

        print(" Entering password")
        self.page.fill(self.password_input, password)

        print("Clicking login button")
        self.page.click(self.login_button)

        #  Give ERPNext time to render popup
        self.page.wait_for_timeout(3000)

        self._handle_permission_popup()

    def _handle_permission_popup(self):
        """
        Close ERPNext 'Not permitted' popup if it appears.
        """
        try:
            if self.page.is_visible(self.permission_popup):
                print("⚠ Permission popup detected, closing it")
                self.page.click(self.popup_close_btn)
                self.page.wait_for_timeout(1000)
        except PlaywrightTimeoutError:
            pass
