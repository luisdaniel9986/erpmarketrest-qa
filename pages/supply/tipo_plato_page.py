import re


class TipoPlatoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_tipos_plato(self):
        self.page.goto("/menu/tipos_plato")

    def crear_tipo_plato(self, nombre):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.locator("#type-dish-modal-name").fill(nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def editar_tipo_plato(self, nombre_actual, nuevo_nombre):
        fila = self._abrir_opciones(nombre_actual)
        fila.get_by_text("Editar").click()
        self.page.locator("#type-dish-modal-name").fill(nuevo_nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()

    def eliminar_tipo_plato(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def cancelar_eliminacion(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def tipo_plato(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("NUEVO"))

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila(nombre)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
