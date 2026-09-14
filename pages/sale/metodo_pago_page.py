import re


class MetodoPagoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_metodos_pago(self):
        self.page.goto("/ventas/metodos_pago/metodo_pago/index")

    def crear_metodo_pago(self, descripcion):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_label(re.compile("DESCRIPCIÓN")).fill(descripcion)
        self.page.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, REGISTRAR")).click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_role("button", name="Cerrar").click()

    def editar_metodo_pago(self, descripcion_actual, nueva_descripcion):
        fila = self._abrir_opciones(descripcion_actual)
        fila.get_by_text("Editar").click()
        self.page.get_by_label(re.compile("DESCRIPCIÓN")).fill(nueva_descripcion)
        self.page.get_by_role("button", name=re.compile("Actualizar")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, ACTUALIZAR")).click()

    def eliminar_metodo_pago(self, descripcion):
        fila = self._abrir_opciones(descripcion)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def cancelar_eliminacion(self, descripcion):
        fila = self._abrir_opciones(descripcion)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def ir_a_cuentas(self, descripcion):
        fila = self._abrir_opciones(descripcion)
        fila.get_by_test_id(re.compile("btn-accounts-")).click()

    def metodo_pago(self, descripcion):
        return self.page.get_by_text(descripcion, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("NUEVO"))

    def _fila(self, descripcion):
        return self.page.locator("tr").filter(has_text=descripcion)

    def _abrir_opciones(self, descripcion):
        fila = self._fila(descripcion)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
