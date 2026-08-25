import re

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class NotaSalidaPage:
    def __init__(self, page):
        self.page = page

    def ir_a_notas_salida(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Nota Salida", exact=True).click()

    def abrir_nueva(self):
        self.page.get_by_role("link", name=re.compile("NUEVO")).click()
        self.page.wait_for_url("**/inventario/nota-salida/create")

    def volver_desde_nueva(self):
        self.abrir_nueva()
        self.page.get_by_role("link", name=re.compile("VOLVER")).click()
        self.page.wait_for_url("**/inventario/nota-salida/index")

    def filtrar(self, fecha_inicio, fecha_fin, tipo=None, estado=None):
        self.page.locator("#note-release-filter-date-start").fill(fecha_inicio)
        self.page.locator("#note-release-filter-date-end").fill(fecha_fin)
        if tipo:
            self._seleccionar_tom("note-release-filter-type", tipo)
        if estado:
            self._seleccionar_tom("note-release-filter-status", estado)
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def limpiar(self):
        self.page.get_by_role("button", name=re.compile("Limpiar")).click()

    def buscar_en_tabla(self, texto):
        buscador = self.page.locator("input[type='search']:visible")
        buscador.fill(texto)
        return buscador

    def abrir_primer_detalle(self):
        self.page.locator("button[data-testid^='row-actions-']").first.click()
        self.page.locator("button[data-testid^='btn-show-']:visible").click()

    def modal_activo(self):
        return self.page.locator(".modal.show")

    def cerrar_modal(self):
        self.modal_activo().get_by_role("button", name=re.compile("Cerrar")).click()

    def cerrar_modal_con_x(self):
        self.page.locator(".modal.show .btn-close").click()

    def abrir_selector_productos(self):
        self.page.get_by_role("button", name=re.compile("Buscar", re.IGNORECASE)).click()

    def seleccionar_primer_producto(self):
        self.page.locator("tr[data-testid^='product-row-']:visible").first.click()

    def filtrar_selector_productos(self, categoria, marca):
        self.page.locator("#products-modal-category").select_option(label=categoria)
        self.page.locator("#products-modal-brand").select_option(label=marca)

    def buscar_en_selector_productos(self, texto):
        buscador = self.page.locator("input[type='search']:visible")
        buscador.fill(texto)
        return buscador

    def cerrar_selector_productos(self):
        self.page.get_by_role("button", name=re.compile("Cerrar")).last.click()

    def cerrar_selector_productos_con_x(self):
        self.page.locator(".btn-close:visible").last.click()

    def agregar_primer_producto(self, cantidad="1"):
        self.abrir_selector_productos()
        self.seleccionar_primer_producto()
        self.page.locator("#note-release-quantity").fill(cantidad)
        self.page.get_by_role("button", name=re.compile("AGREGAR")).click()

    def editar_producto_agregado(self, cantidad):
        self.abrir_edicion_producto_agregado()
        modal = self.page.locator(".modal.show")
        modal.locator("input[type='number']").fill(cantidad)
        modal.get_by_role(
            "button", name=re.compile("Guardar|Actualizar|Aceptar", re.IGNORECASE)
        ).click()

    def abrir_edicion_producto_agregado(self):
        self.page.locator("button[data-testid^='btn-edit-row-']").click()

    def cerrar_edicion_producto(self):
        self.page.locator(".modal.show").get_by_role(
            "button", name="Cerrar", exact=True
        ).click()

    def cerrar_edicion_producto_con_x(self):
        self.page.locator(".modal.show .btn-close").click()

    def eliminar_producto_agregado(self):
        self.page.locator("button[data-testid^='btn-delete-row-']").click()

    def seleccionar_almacenes_y_tipo(self, origen, destino, tipo):
        self._seleccionar_tom("note-release-warehouse-origin", origen)
        self._seleccionar_tom("note-release-warehouse-destiny", destino)
        self._seleccionar_tom("note-release-type", tipo)

    def limpiar_selector_con_x(self, selector_id):
        self.page.get_by_test_id(selector_id).get_by_role("button").click()

    def registrar_nota(self):
        self.page.locator("#note-release-observation").fill(
            "Nota de salida creada por pruebas QA"
        )
        self.page.get_by_role("button", name=re.compile("REGISTRAR")).click()
        try:
            self.page.locator(".swal2-confirm").click(timeout=5_000)
        except PlaywrightTimeoutError:
            pass
        self.page.wait_for_url("**/inventario/nota-salida/index", timeout=60_000)

    def boton_paginacion(self, nombre):
        return self.page.locator(f"button[aria-label='{nombre}']:visible")

    def ir_a_pagina(self, nombre):
        self.boton_paginacion(nombre).click()

    def _seleccionar_tom(self, selector_id, opcion):
        componente = self.page.locator(f"#{selector_id}").locator(
            "xpath=following-sibling::*[contains(@class, 'ts-wrapper')][1]"
        )
        componente.locator(".ts-control").click()
        componente.locator(".ts-dropdown").get_by_role(
            "option", name=re.compile(re.escape(opcion), re.IGNORECASE)
        ).click()
