import re


class SedePage:
    def __init__(self, page):
        self.page = page

    def ir_a_sedes(self):
        self.page.goto("/mantenimiento/sedes/index")

    def crear(self, nombre, direccion="AV. QA 123"):
        self._abrir_creacion()
        self.page.locator("#branch-create-name").fill(nombre)
        self.page.locator("#branch-create-address").fill(direccion)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, REGISTRAR")).click()
        self.page.wait_for_url("**/mantenimiento/sedes/index", timeout=30_000)

    def cancelar_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Cancelar")).click()
        self.page.wait_for_url("**/mantenimiento/sedes/index")

    def eliminar(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def sede(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("Nueva Sede"))

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=re.compile(re.escape(nombre)))

    def _abrir_creacion(self):
        self.page.get_by_role("link", name=re.compile("Nueva Sede")).click()
        self.page.wait_for_url("**/mantenimiento/sedes/create")
