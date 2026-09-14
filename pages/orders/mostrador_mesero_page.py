import re


class MostradorMeseroPage:
    """Smoke-level a proposito: el flujo real de tomar un pedido dispara
    cocina/KDS y puede derivar en una venta real (SUNAT) al cerrarlo, asi
    que este objeto solo cubre navegacion y filtros, nunca crea un pedido."""

    def __init__(self, page):
        self.page = page

    def ir_a_mostrador_mesero(self):
        self.page.goto("/mostrador")

    def buscar_mesa(self, texto):
        self.page.locator("#floor-plan-search").fill(texto)

    def filtrar_libres(self):
        self.page.get_by_role("button", name=re.compile("Libres")).click()

    def filtrar_todas(self):
        self.page.get_by_role("button", name=re.compile("Todas")).click()

    def actualizar(self):
        self.page.get_by_role("button", name=re.compile("Actualizar")).click()

    def grid_de_mesas(self):
        return self.page.locator(".floor-plan-grid")

    def titulo(self):
        return self.page.get_by_role("heading", name=re.compile("Mostrador Mesero"))
