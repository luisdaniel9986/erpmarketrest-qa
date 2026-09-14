import re


class UsuarioPage:
    def __init__(self, page):
        self.page = page

    def ir_a_usuarios(self):
        self.page.goto("/mantenimiento/usuario/index")

    def crear(self, correo, colaborador, password="Qatest123"):
        # El combo de Colaborador lista a TODOS los que aún no tienen
        # usuario — puede incluir gente real del tenant, así que siempre se
        # busca por nombre exacto en vez de tomar "la primera opción".
        self._abrir_creacion()
        self._seleccionar_opcion("user-create-collaborator", colaborador)
        self.page.locator("#user-create-email").fill(correo)
        self.page.locator("#user-create-password").fill(password)
        self.page.locator("#user-create-password-repeat").fill(password)
        self._seleccionar_primera_opcion("user-create-roles")
        self.page.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, REGISTRAR")).click()
        self.page.wait_for_url("**/mantenimiento/usuario/index", timeout=30_000)

    def cancelar_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Volver")).click()
        self.page.wait_for_url("**/mantenimiento/usuario/index")

    def eliminar(self, correo):
        fila = self._fila(correo)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def usuario(self, correo):
        return self.page.get_by_text(correo, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("NUEVO"))

    def _seleccionar_primera_opcion(self, test_id):
        self.page.get_by_test_id(test_id).click()
        self.page.get_by_test_id(test_id).get_by_role("option").first.click()

    def _seleccionar_opcion(self, test_id, texto):
        combo = self.page.get_by_test_id(test_id)
        combo.click()
        combo.get_by_role("option", name=re.compile(re.escape(texto))).first.click()

    def _fila(self, correo):
        return self.page.locator("tr").filter(has_text=correo)

    def _abrir_creacion(self):
        self.page.get_by_role("link", name=re.compile("NUEVO")).click()
        self.page.wait_for_url("**/mantenimiento/usuario/create")
