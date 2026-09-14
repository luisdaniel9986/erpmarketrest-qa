import re


class MostradorCajeroPage:
    """El flujo "Cobrar" emite el comprobante de una orden real (potencialmente
    hacia SUNAT), así que no se automatiza aquí — solo se cubre listado/filtros."""

    def __init__(self, page):
        self.page = page

    def ir_a_mostrador_cajero(self):
        self.page.goto("/mostrador_cajero/index")

    def titulo(self):
        return self.page.get_by_role("heading", name="Mostrador Cajero")

    def filtrar_por_estado(self, estado):
        combo = self.page.get_by_test_id("cashier-counter-status")
        combo.click()
        combo.locator(".ts-dropdown .option", has_text=estado).first.click()

    def establecer_fechas(self, desde, hasta):
        self.page.get_by_label("Desde").fill(desde)
        self.page.get_by_label("Hasta").fill(hasta)

    def filtrar(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def tabla(self):
        return self.page.locator("#table_cashier_counter")
