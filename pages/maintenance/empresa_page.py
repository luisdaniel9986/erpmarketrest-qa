import re


class EmpresaPage:
    def __init__(self, page):
        self.page = page

    def ir_a_empresas(self):
        self.page.goto("/mantenimiento/empresa/index")

    def editar_primera_empresa(self):
        self.page.locator("tbody tr").first.get_by_role(
            "button", name=re.compile("Editar")
        ).click()
        self.page.wait_for_url(re.compile(r"/mantenimiento/empresa/edit/\d+"))

    def campo_telefono(self):
        return self.page.locator("#company-phone")

    def actualizar_telefono(self, telefono):
        self.campo_telefono().fill(telefono)
        self.page.get_by_role("button", name=re.compile("Guardar$")).click()
        alerta = self.page.locator(".swal2-popup")
        alerta.wait_for(state="visible")
        alerta.wait_for(state="hidden", timeout=5_000)

    def titulo(self):
        return self.page.get_by_role("heading", name=re.compile("Datos de la Empresa"))
