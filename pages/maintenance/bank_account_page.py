import re


class BankAccountPage:
    def __init__(self, page):
        self.page = page

    def ir_a_cuentas_bancarias(self):
        self.page.goto("/mantenimiento/cuentas/index")

    def crear_cuenta(self, nombre, titular, numero_cuenta, banco="INTERBANK", cci=None):
        self.page.get_by_role("button", name=re.compile("Nueva Cuenta")).click()
        modal = self._modal_crear()
        modal.get_by_label("Nombre").fill(nombre)
        modal.get_by_label("Titular").fill(titular)
        combo = self.page.get_by_test_id("bank-account-bank")
        combo.click()
        combo.locator(".ts-dropdown .option", has_text=banco).first.click()
        modal.get_by_label("N° Cuenta").fill(numero_cuenta)
        # El campo CCI no se muestra como obligatorio en el formulario (sin
        # asterisco/required_field) pero el backend lo exige igual — ver
        # docs/isuues, es un bug real de la app, no del test.
        modal.get_by_label("CCI").fill(cci or numero_cuenta)
        modal.get_by_role("button", name=re.compile("Guardar|Registrar")).click()
        self.page.get_by_role("button", name="SÍ, REGISTRAR").click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("Nueva Cuenta")).click()
        self._modal_crear().get_by_role("button", name="Cancelar").click()

    def buscar_cuenta(self, texto):
        self.page.locator(".dt-search input").fill(texto)

    def editar_cuenta(self, nombre_actual, nuevo_nombre):
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

    def eliminar_cuenta(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Sí, eliminar").click()

    def cuenta(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("Nueva Cuenta"))

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def _modal_crear(self):
        return self.page.locator("#mdl-create-account")

    def _modal_editar(self):
        return self.page.locator("#mdl-edit-account")

    def _fila_de_cuenta(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila_de_cuenta(nombre)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
