import re


class AlmacenPage:
    def __init__(self, page):
        self.page = page

    def ir_a_almacenes(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Almacenes").click()

    def crear_almacen(self, nombre, sede):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_role("textbox", name="Nombre *").fill(nombre)
        self.page.get_by_test_id("warehouse-branch").click()
        self.page.get_by_test_id("warehouse-branch").get_by_role(
            "option", name=sede, exact=True
        ).click()
        self._guardar()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def cerrar_creacion(self):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self._cerrar_modal_con_x()

    def filtrar_por_estado(self, estado):
        self.page.locator("div").filter(has_text=re.compile("^Solo activos$")).first.click()
        self.page.get_by_role("option", name=estado, exact=True).click()
        self.aplicar_filtro()

    def aplicar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def limpiar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Limpiar")).click()

    def ver_detalle(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-view-")).click()

    def cerrar_detalle(self):
        self.page.get_by_role("button", name=re.compile("Cerrar")).click()

    def cerrar_detalle_con_x(self, nombre):
        self.ver_detalle(nombre)
        self._cerrar_modal_con_x()

    def editar(self, nombre):
        self._abrir_edicion(nombre)
        self._guardar()

    def cancelar_edicion(self, nombre):
        self._abrir_edicion(nombre)
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def cerrar_edicion(self, nombre):
        self._abrir_edicion(nombre)
        self._cerrar_modal_con_x()

    def cancelar_eliminacion(self, nombre):
        self._abrir_eliminacion(nombre)
        self.page.get_by_role("button", name="Cancelar").click()

    def eliminar(self, nombre):
        self._abrir_eliminacion(nombre)
        self.page.get_by_role("button", name="Sí, eliminar").click()

    def reactivar(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-activate-")).click()
        self.page.get_by_role("button", name="Sí, activar").click()

    def almacen(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("NUEVO"))

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def modal(self):
        return self.page.get_by_role("dialog")

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_eliminacion(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()

    def _abrir_edicion(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-edit-")).click()

    def _cerrar_modal_con_x(self):
        self.modal().locator(".btn-close").click()

    def _guardar(self):
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()
