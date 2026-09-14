import re


class ResumenesPage:
    def __init__(self, page):
        self.page = page

    def ir_a_resumenes(self):
        self.page.get_by_role("button", name=re.compile("Ventas")).click()
        self.page.get_by_role("link", name="Resumen Diario", exact=True).click()

    def filtrar_por_estado(self, estado):
        self.page.locator("#summary-filter-status").select_option(estado)

    def filtrar_por_fechas(self, inicio, fin):
        self.page.locator("#summary-filter-date-start").fill(inicio)
        self.page.locator("#summary-filter-date-end").fill(fin)

    def tabla(self):
        return self.page.locator("#table_summaries")

    def abrir_modal_nuevo(self):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()

    def modal_nuevo_resumen(self):
        return self.page.locator("#mdl-create-summary")

    def cerrar_modal_nuevo(self):
        self.modal_nuevo_resumen().get_by_role("button", name=re.compile("Cancelar")).click()
