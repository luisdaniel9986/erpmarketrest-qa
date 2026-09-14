import re


class ReporteContablePage:
    def __init__(self, page):
        self.page = page

    def ir_a_reporte_contable(self):
        self.page.get_by_role("button", name=re.compile("Contabilidad")).click()
        self.page.get_by_role("link", name="Reporte Contable", exact=True).click()

    def filtrar_por_fechas(self, inicio, fin):
        self.page.locator("#accounting-report-date-start").fill(inicio)
        self.page.locator("#accounting-report-date-end").fill(fin)
        self.aplicar_filtro()

    def filtrar_por_estado(self, estado):
        self.page.locator("#accounting-report-status").select_option(estado)
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
