import re


class KardexPage:
    def __init__(self, page, valorizado=False):
        self.page = page
        self.valorizado = valorizado

    def ir_a_kardex(self):
        nombre = "Kardex Valorizado" if self.valorizado else "Kardex"
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name=nombre, exact=True).click()

    def seleccionar_producto(self, busqueda="a"):
        producto = self.page.get_by_role("combobox", name=re.compile("PRODUCTO"))
        producto.click()
        producto.fill(busqueda)
        prefijo = "valued-kardex-product" if self.valorizado else "kardex-product"
        self.page.locator(f"[id^='{prefijo}-opt-']").first.click()

    def selector_producto(self):
        prefijo = "valued-kardex-product" if self.valorizado else "kardex-product"
        return self.page.locator(f"#{prefijo}")

    def limpiar_producto_con_x(self):
        componente = self.selector_producto().locator(
            "xpath=following-sibling::*[contains(@class, 'ts-wrapper')][1]"
        )
        componente.get_by_role("button").click()

    def seleccionar_almacen(self, almacen):
        prefijo = "valued-kardex" if self.valorizado else "kardex"
        self.page.locator(f"#{prefijo}-warehouse").select_option(label=almacen)

    def establecer_fechas(self, fecha_inicio, fecha_fin):
        prefijo = "valued-kardex" if self.valorizado else "kardex"
        self.page.locator(f"#{prefijo}-date-start").fill(fecha_inicio)
        self.page.locator(f"#{prefijo}-date-end").fill(fecha_fin)

    def filtrar(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def limpiar(self):
        self.page.get_by_role("button", name=re.compile("Limpiar")).click()

    def abrir_pdf(self):
        with self.page.expect_popup() as popup:
            self.page.get_by_role("link", name=re.compile("PDF")).click()
        return popup.value

    def exportar_excel(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_role("link", name=re.compile("EXCEL")).click()
        return descarga.value

    def buscar_en_tabla(self, texto):
        buscador = self.page.get_by_role("searchbox", name=re.compile("Buscar"))
        buscador.fill(texto)
        return buscador

    def texto_primera_fila(self):
        return self.page.locator("tbody tr").first.inner_text()

    def boton_paginacion(self, nombre):
        return self.page.locator(f"button[aria-label='{nombre}']")

    def ir_a_pagina(self, nombre):
        self.boton_paginacion(nombre).click()
