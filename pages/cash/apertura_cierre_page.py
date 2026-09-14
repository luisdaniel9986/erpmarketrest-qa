import re


class AperturaCierrePage:
    """Abrir/cerrar una caja es la operación normal de todos los días para un
    cajero (no una acción de 'zona de peligro') — se automatiza el ciclo
    completo, siempre abriendo y cerrando dentro del mismo test para no dejar
    turnos abiertos sueltos en el ambiente."""

    def __init__(self, page):
        self.page = page

    def ir_a_apertura_cierre(self):
        self.page.goto("/cajas/movimientos/apertura-cierre")

    def titulo(self):
        return self.page.get_by_role("heading", name="LISTA DE APERTURAS DE CAJA")

    def boton_nuevo(self):
        return self.page.get_by_role("button", name="NUEVO")

    def abrir_caja(self, saldo_inicial="100"):
        self.boton_nuevo().click()
        modal = self.page.locator("#mdl-open-cash")
        combo = modal.get_by_test_id("open-cash-select")
        combo.click()
        combo.locator(".ts-dropdown .option").first.click()
        modal.locator("#open-cash-shift").select_option(index=1)
        modal.locator("#open-cash-initial-amount").fill(saldo_inicial)
        # En modo HIBRIDO exige al menos un mesero/vendedor asignado a la caja.
        modal.locator('[data-testid^="server-check-"]').first.check()
        modal.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()
        modal.wait_for(state="hidden", timeout=10_000)

    def fila_abierta(self):
        return self.page.locator("tr").filter(has_text="ABIERTO").first

    def cerrar_ultima_caja_abierta(self, saldo_real="100"):
        fila = self.fila_abierta()
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_text("Cerrar caja").click()
        modal = self.page.locator("#mdl-close-cash")
        modal.get_by_text("CONSOLIDADO").wait_for(state="visible", timeout=15_000)
        modal.locator("#close-cash-real-amount").fill(saldo_real)
        modal.get_by_role("button", name=re.compile("Cerrar Caja")).click()
        self.page.get_by_role("button", name="Sí!").click()
        modal.wait_for(state="hidden", timeout=10_000)
