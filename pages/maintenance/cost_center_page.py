import re


class CostCenterPage:
    def __init__(self, page):
        self.page = page

    def ir_a_centros_costo(self):
        self.page.goto("/mantenimiento/centros_costo/index")

    def crear_centro_costo(self, nombre):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()
        modal = self._modal_crear()
        modal.get_by_label("Nombre").fill(nombre)
        modal.get_by_role("button", name=re.compile("Guardar|Registrar")).click()
        self.page.get_by_role("button", name="SÍ, REGISTRAR").click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()
        self._modal_crear().get_by_role("button", name="Cancelar").click()

    def buscar_centro_costo(self, texto):
        self.page.locator(".dt-search input").fill(texto)

    def editar_centro_costo(self, nombre_actual, nuevo_nombre):
        fila = self._abrir_opciones(nombre_actual)
        fila.get_by_text("Editar").click()
        modal = self._modal_editar()
        modal.get_by_label("Nombre").fill(nuevo_nombre)
        modal.get_by_role("button", name=re.compile("Actualizar")).click()
        self.page.get_by_role("button", name="SÍ, ACTUALIZAR").click()

    def cancelar_eliminacion(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Cancelar").click()

    def eliminar_centro_costo(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Sí, eliminar").click()

    def centro_costo(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("Nuevo"))

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def _modal_crear(self):
        return self.page.locator("#mdl-create-cost-center")

    def _modal_editar(self):
        return self.page.locator("#mdl-edit-cost-center")

    def _fila_de_centro_costo(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila_de_centro_costo(nombre)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
