import re


class ProveedorPage:
    def __init__(self, page):
        self.page = page

    def ir_a_proveedores(self):
        self.page.goto("/compras/proveedores/index")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("Nuevo")).click()

    def crear_proveedor(self, nombre, nro_documento):
        self.ir_a_crear()
        # El tipo de documento (TomSelect) ya viene preseleccionado en RUC.
        self.page.locator("#supplier-document-number").fill(nro_documento)
        self.page.locator("#supplier-name").fill(nombre)
        self.page.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name=re.compile("Sí, registrar")).click()
        self.page.wait_for_url(re.compile(r"/proveedores/index"))

    def consultar_documento(self):
        self.page.get_by_test_id("btn-consultar-documento").click()

    def campo_nro_documento(self):
        return self.page.locator("#supplier-document-number")

    def campo_nombre(self):
        return self.page.locator("#supplier-name")

    def volver(self):
        self.page.get_by_role("link", name=re.compile("Volver")).click()

    def editar_proveedor(self, nombre_actual, nuevo_nombre):
        fila = self._abrir_opciones(nombre_actual)
        fila.get_by_text("Editar").click()
        self.page.locator("#supplier-name").fill(nuevo_nombre)
        self.page.get_by_role("button", name=re.compile("Actualizar")).click()
        self.page.get_by_role("button", name=re.compile("Sí, actualizar")).click()
        self.page.wait_for_url(re.compile(r"/proveedores/index"))

    def eliminar_proveedor(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def cancelar_eliminacion(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def proveedor(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("Nuevo"))

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila(nombre)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
