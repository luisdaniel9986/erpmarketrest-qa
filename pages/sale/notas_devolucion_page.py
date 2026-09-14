import re


class NotasDevolucionPage:
    def __init__(self, page):
        self.page = page

    def ir_a_notas_devolucion(self):
        self.page.get_by_role("button", name=re.compile("Ventas")).click()
        self.page.get_by_role("link", name="Notas Devolución", exact=True).click()

    def filtrar_por_fechas(self, inicio, fin):
        self.page.locator("#return-note-filter-date-start").fill(inicio)
        self.page.locator("#return-note-filter-date-end").fill(fin)
        self.aplicar_filtro()

    def aplicar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def tabla(self):
        return self.page.locator("table.table-hover")
