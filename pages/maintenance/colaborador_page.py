import re


class ColaboradorPage:
    def __init__(self, page):
        self.page = page

    def ir_a_colaboradores(self):
        self.page.goto("/mantenimiento/colaborador/index")

    def crear(self, nombre, dni, telefono, dias_trabajo="30", dias_descanso="0", salario="1500"):
        self._abrir_creacion()
        self.page.locator("#collaborator-create-doc-number").fill(dni)
        self.page.locator("#collaborator-create-full-name").fill(nombre)
        self._seleccionar_primera_opcion("collaborator-create-position")
        self._seleccionar_primera_opcion("collaborator-create-branch")
        self.page.locator("#collaborator-create-phone").fill(telefono)
        self.page.locator("#collaborator-create-work-days").fill(dias_trabajo)
        self.page.locator("#collaborator-create-rest-days").fill(dias_descanso)
        self.page.locator("#collaborator-create-salary").fill(salario)
        self.page.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name=re.compile("Sí, registrar")).click()
        self.page.wait_for_url("**/mantenimiento/colaborador/index", timeout=30_000)

    def cancelar_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Volver")).click()
        self.page.wait_for_url("**/mantenimiento/colaborador/index")

    def eliminar(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def colaborador(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("Nuevo"))

    def _seleccionar_primera_opcion(self, test_id):
        self.page.get_by_test_id(test_id).click()
        self.page.get_by_test_id(test_id).get_by_role("option").first.click()

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=re.compile(re.escape(nombre)))

    def _abrir_creacion(self):
        self.page.get_by_role("link", name=re.compile("Nuevo")).click()
        self.page.wait_for_url("**/mantenimiento/colaborador/create")
