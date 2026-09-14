import re


class VentasPlatosPage:
    def __init__(self, page):
        self.page = page

    def ir_a_ventas_platos(self):
        self.page.get_by_role("button", name=re.compile("Reportes")).click()
        self.page.get_by_role("link", name="Ventas Platos", exact=True).click()

    def filtrar_por_fechas(self, inicio, fin):
        self.page.locator("#dish-sales-report-start-date").fill(inicio)
        self.page.locator("#dish-sales-report-end-date").fill(fin)
        self.aplicar_filtro()

    def aplicar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def abrir_pdf(self):
        with self.page.expect_popup() as popup:
            self.page.get_by_role("link", name=re.compile("PDF")).click()
        return popup.value

    def exportar_excel(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_role("link", name=re.compile("Excel")).click()
        return descarga.value
