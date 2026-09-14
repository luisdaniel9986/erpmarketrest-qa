import re


class VentasProductosPage:
    def __init__(self, page):
        self.page = page

    def ir_a_ventas_productos(self):
        self.page.get_by_role("button", name=re.compile("Reportes")).click()
        self.page.get_by_role("link", name="Ventas Productos", exact=True).click()

    def filtrar_por_fechas(self, inicio, fin):
        self.page.locator("#product-sales-report-start-date").fill(inicio)
        self.page.locator("#product-sales-report-end-date").fill(fin)
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
