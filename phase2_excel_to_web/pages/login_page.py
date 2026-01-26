from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


class LoginPage:
    """
    Generic Login Page Object.
    Can be reused for multiple OEM portals.
    """

    def __init__(self, page: Page):
        self.page = page

        #  DEFAULT SELECTORS (can be overridden per OEM later)
        self.username_input = "input[name='username'], input[type='text']"
        self.password_input = "input[name='password'], input[type='password']"
        self.login_button = "button[type='submit'], input[type='submit']"

    def open(self, url: str):
        """
        Open login URL and wait until page is ready.
        """
        try:
            print(f" Opening URL: {url}")
            self.page.goto(url, timeout=60000, wait_until="load")
        except PlaywrightTimeoutError:
            raise RuntimeError(f" Page load timed out for URL: {url}")

    def login(self, username: str, password: str):
        """
        Perform login action.
        """
        try:
            print(" Waiting for username field...")
            self.page.wait_for_selector(self.username_input, timeout=30000)

            print(" Entering username")
            self.page.fill(self.username_input, username)

            print(" Entering password")
            self.page.fill(self.password_input, password)

            print(" Clicking login button")
            self.page.click(self.login_button)

            # Optional: wait for navigation / dashboard
            self.page.wait_for_timeout(3000)

        except PlaywrightTimeoutError:
            raise RuntimeError(" Login elements not found or page too slow")

    def login_and_wait(self, username: str, password: str, success_selector: str | None = None):
        """
        Login and optionally wait for a success element (dashboard).
        """
        self.login(username, password)

        if success_selector:
            try:
                print(" Waiting for successful login indicator...")
                self.page.wait_for_selector(success_selector, timeout=30000)
            except PlaywrightTimeoutError:
                raise RuntimeError(" Login failed or dashboard not loaded")
