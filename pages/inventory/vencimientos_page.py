import re


class VencimientosPage:
    def __init__(self, page):
        self.page = page

    def ir_a_vencimientos(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Vencimientos", exact=True).click()

    def filtrar(self, almacen, dias):
        self.page.locator("#product-batch-warehouse").select_option(label=almacen)
        self.page.locator("#product-batch-days").fill(str(dias))
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def limpiar(self):
        self.page.get_by_role("button", name=re.compile("Limpiar")).click()

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

    def abrir_primera_baja(self):
        self.page.get_by_role(
            "button", name=re.compile("Dar de baja", re.IGNORECASE)
        ).first.click()

    def cantidad_baja(self):
        return self.page.locator("#swal2-input")

    def cancelar_baja(self):
        self.page.get_by_role("button", name="Cancelar", exact=True).click()

    def alerta_baja(self):
        return self.page.locator(".swal2-container")

    def boton_paginacion(self, nombre):
        return self.page.locator(f"button[aria-label='{nombre}']:visible")

    def ir_a_pagina(self, nombre):
        self.boton_paginacion(nombre).click()
