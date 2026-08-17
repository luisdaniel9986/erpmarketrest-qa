class LoginPage:
    def __init__(self, page):
        self.page = page

    def ir_a_login(self):
        self.page.goto("/login")

    def login(self, email, password):
        self.page.get_by_label("Correo Electrónico").fill(email)
        self.page.get_by_label("Contraseña").fill(password)
        self.page.get_by_role("button", name="Iniciar Sesión").click()

    def mensaje_error(self):
        return self.page.locator(".alert-danger")
