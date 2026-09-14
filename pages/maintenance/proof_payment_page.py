import re


class ProofPaymentPage:
    def __init__(self, page):
        self.page = page

    def ir_a_comprobantes(self):
        self.page.goto("/mantenimiento/comprobantes/index")

    def crear_comprobante(self, descripcion):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()
        modal = self._modal_crear()
        modal.get_by_label("Descripción").fill(descripcion)
        modal.get_by_role("button", name=re.compile("Guardar|Registrar")).click()
        self.page.get_by_role("button", name="SÍ, REGISTRAR").click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()
        self._modal_crear().get_by_role("button", name="Cancelar").click()

    def buscar_comprobante(self, texto):
        self.page.locator(".dt-search input").fill(texto)

    def editar_comprobante(self, descripcion_actual, nueva_descripcion):
        fila = self._abrir_opciones(descripcion_actual)
        fila.get_by_text("Editar").click()
        modal = self._modal_editar()
        modal.get_by_label("Descripción").fill(nueva_descripcion)
        modal.get_by_role("button", name=re.compile("Actualizar")).click()
        self.page.get_by_role("button", name="SÍ, ACTUALIZAR").click()

    def cancelar_eliminacion(self, descripcion):
        fila = self._abrir_opciones(descripcion)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Cancelar").click()

    def eliminar_comprobante(self, descripcion):
        fila = self._abrir_opciones(descripcion)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Sí, eliminar").click()

    def comprobante(self, descripcion):
        return self.page.get_by_text(descripcion, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("Nuevo"))

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def _modal_crear(self):
        return self.page.locator("#mdl-create-proof-payment-crud")

    def _modal_editar(self):
        return self.page.locator("#mdl-edit-proof-payment-crud")

    def _fila_de_comprobante(self, descripcion):
        return self.page.locator("tr").filter(has_text=descripcion)

    def _abrir_opciones(self, descripcion):
        fila = self._fila_de_comprobante(descripcion)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
