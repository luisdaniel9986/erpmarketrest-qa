class LoginPage:
    def __init__(self, page):
        self.page = page

    def ir_a_login(self):
        self.page.goto("/login")

    def login(self, email, password):
        self.page.get_by_test_id("login-email").fill(email)
        self.page.get_by_test_id("login-password").fill(password)
        self.page.get_by_test_id("login-submit").click()

    def mensaje_error(self):
        return self.page.get_by_role("alert")