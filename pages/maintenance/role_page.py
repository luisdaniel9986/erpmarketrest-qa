import re


class RolePage:
    def __init__(self, page):
        self.page = page

    def ir_a_roles(self):
        self.page.goto("/mantenimiento/roles/index")

    def crear(self, nombre):
        self._abrir_creacion()
        self.page.locator("#role-create-nombre").fill(nombre)
        self.marcar_todos_los_permisos()
        self.page.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, REGISTRAR")).click()
        self.page.wait_for_url("**/mantenimiento/roles/index", timeout=30_000)

    def cancelar_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Volver")).click()
        self.page.wait_for_url("**/mantenimiento/roles/index")

    def marcar_todos_los_permisos(self):
        self.page.get_by_role("button", name=re.compile("Marcar todos")).click()

    def eliminar(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def rol(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("Nuevo"))

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=re.compile(re.escape(nombre)))

    def _abrir_creacion(self):
        self.page.get_by_role("link", name=re.compile("Nuevo")).click()
        self.page.wait_for_url("**/mantenimiento/roles/create")
