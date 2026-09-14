import re


class CuentasProveedoresPage:
    """Pagar/anular una cuenta real de proveedor no se automatiza acá — requeriría
    una deuda creada por QA a través de Compras a crédito, fuera de este alcance
    inicial. Se cubre listado y filtros."""

    def __init__(self, page):
        self.page = page

    def ir_a_cuentas_proveedores(self):
        self.page.goto("/cuentas/proveedores")

    def titulo(self):
        return self.page.get_by_role("heading", name="Cuentas por Pagar")

    def filtrar_por_estado(self, estado):
        self.page.get_by_label("Estado:").select_option(label=estado)

    def filtrar(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def boton_pagar_seleccionadas(self):
        return self.page.get_by_role("button", name=re.compile("Pagar seleccionadas"))
