import re


class InventarioPage:
    def __init__(self, page):
        self.page = page

    def ir_a_inventario(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Inventario", exact=True).click()

    def filtrar(self, almacen, stock):
        self.page.get_by_label("ALMACÉN").select_option(almacen)
        self.page.get_by_label("STOCK", exact=True).select_option(stock)
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def abrir_pdf(self):
        with self.page.expect_popup() as popup:
            self.page.get_by_role("link", name=re.compile("PDF")).click()
        return popup.value

    def exportar_excel(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_role("link", name=re.compile("EXCEL")).click()
        return descarga.value

    def buscar_en_tabla(self, texto):
        buscador = self.page.get_by_role("searchbox")
        buscador.fill(texto)
        return buscador

    def texto_primera_fila(self):
        return self.page.locator("tbody tr").first.inner_text()
