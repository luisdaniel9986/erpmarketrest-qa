import re


class CuentasClientesPage:
    """Mismo criterio que CuentasProveedoresPage: no se paga/anula una cuenta
    real de cliente, solo se cubre listado y filtros."""

    def __init__(self, page):
        self.page = page

    def ir_a_cuentas_clientes(self):
        self.page.goto("/cuentas/clientes")

    def titulo(self):
        return self.page.get_by_role("heading", name="Cuentas por Cobrar")

    def filtrar_por_estado(self, estado):
        self.page.get_by_label("Estado:").select_option(label=estado)

    def filtrar(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def boton_pagar_seleccionadas(self):
        return self.page.get_by_role("button", name=re.compile("Cobrar seleccionadas"))
