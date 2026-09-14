import re


class ValorizacionInventarioPage:
    def __init__(self, page):
        self.page = page

    def ir_a_valorizacion(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Valorización Inventario", exact=True).click()

    def selector_almacen(self):
        return self.page.get_by_label("ALMACÉN")

    def seleccionar_almacen(self, almacen):
        self.page.locator("#inventory-valuation-filter-warehouse").select_option(
            label=almacen
        )

    def exportar_excel(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_role("link", name=re.compile("EXCEL")).click()
        return descarga.value

    def abrir_pdf(self):
        with self.page.expect_popup() as popup:
            self.page.get_by_role("link", name=re.compile("PDF")).click()
        return popup.value

    def buscar_en_tabla(self, texto):
        buscador = self.page.get_by_role("searchbox")
        buscador.fill(texto)
        return buscador

    def texto_primera_fila(self):
        return self.page.locator("tbody tr").first.inner_text()
