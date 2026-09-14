import re


class ProductoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_productos(self):
        self.page.get_by_role("button", name=re.compile("Inventario")).click()
        self.page.get_by_role("link", name="Productos").click()

    def exportar(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_role("button", name=re.compile("EXPORTAR")).click()
        return descarga.value

    def importar(self, ruta_archivo, almacen="CENTRAL"):
        self.page.get_by_role("button", name=re.compile("IMPORTAR")).click()
        with self.page.expect_download():
            self.page.get_by_role("link", name=re.compile("Descargar formato Excel")).click()
        self.page.locator("#product-import-warehouse").select_option(label=almacen)
        self.page.get_by_role("button", name=re.compile("Archivo Excel")).set_input_files(ruta_archivo)
        self.page.get_by_role("button", name=re.compile("Validar")).click()
        self.page.get_by_role("button", name=re.compile(r"Importar 1 producto")).click()
        self.page.get_by_role("button", name=re.compile("Cerrar")).click()

    def cancelar_importacion(self):
        self.page.get_by_role("button", name=re.compile("IMPORTAR")).click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def cerrar_importacion(self):
        self.page.get_by_role("button", name=re.compile("IMPORTAR")).click()
        self.modal().locator(".btn-close").click()

    def cancelar_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Cancelar")).click()
        self.page.wait_for_url("**/inventario/productos/index")

    def volver_desde_creacion(self):
        self._abrir_creacion()
        self.page.get_by_role("link", name=re.compile("Volver")).click()
        self.page.wait_for_url("**/inventario/productos/index")

    def cancelar_nueva_categoria(self):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Categor")
        dialogo.get_by_role("button", name=re.compile("Cancelar")).click()

    def cerrar_nueva_categoria(self):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Categor")
        dialogo.get_by_role("button", name="Close").click()

    def registrar_nueva_categoria(self, nombre):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Categor")
        dialogo.locator("input").fill(nombre)
        dialogo.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name="Sí").click()
        dialogo.wait_for(state="hidden", timeout=30_000)

    def cancelar_nueva_marca(self):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Marca")
        dialogo.get_by_role("button", name=re.compile("Cancelar")).click()

    def cerrar_nueva_marca(self):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Marca")
        dialogo.get_by_role("button", name="Close").click()

    def registrar_nueva_marca(self, nombre):
        self._abrir_creacion()
        dialogo = self._abrir_registro_rapido("Marca")
        dialogo.locator("input").fill(nombre)
        dialogo.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name="Sí").click()
        dialogo.wait_for(state="hidden", timeout=30_000)

    def crear(self, datos, ruta_imagen):
        self._abrir_creacion()
        self.page.get_by_role("textbox", name="Nombre *").fill(datos["nombre"])
        self.page.get_by_test_id("product-category").click()
        self.page.get_by_test_id("product-category").get_by_role(
            "option", name=re.compile(datos["categoria"], re.IGNORECASE)
        ).click()
        self.page.get_by_role("textbox", name=re.compile("Descripción")).fill(datos["descripcion"])
        self.page.get_by_role("combobox", name=re.compile("Marca")).click()
        self.page.locator("#product-brand-ts-dropdown").get_by_role(
            "option", name=re.compile(datos["marca"], re.IGNORECASE)
        ).click()
        self.page.get_by_role("spinbutton", name=re.compile("Precio venta")).fill(datos["precio_venta"])
        self.page.get_by_role("spinbutton", name=re.compile("Precio compra")).fill(datos["precio_compra"])
        self.page.get_by_test_id("product-unit").click()
        self.page.get_by_test_id("product-unit").get_by_role(
            "option", name=re.compile(datos["unidad"], re.IGNORECASE)
        ).click()
        self.page.get_by_role("spinbutton", name=re.compile("Stock inicial")).fill(datos["stock_inicial"])
        self.page.get_by_role("spinbutton", name=re.compile("Stock mínimo")).fill(datos["stock_minimo"])
        self.page.get_by_role("textbox", name=re.compile("Cód. Fábrica")).fill(datos["codigo_fabrica"])
        self.page.get_by_role("textbox", name=re.compile("Cód. Barras")).fill(datos["codigo_barras"])
        self.page.get_by_text("Examina").set_input_files(ruta_imagen)
        self.page.get_by_role("button", name=re.compile("Guardar", re.IGNORECASE)).click()
        self.page.get_by_role("button", name="Sí").click()
        self.page.wait_for_url("**/inventario/productos/index", timeout=60_000)

    def filtrar_por_estado(self, estado):
        selector_estado = self.page.locator("select").filter(
            has=self.page.locator("option", has_text=re.compile("^ANULADO$"))
        )
        control_estado = selector_estado.locator(
            "xpath=following-sibling::*[contains(@class, 'ts-wrapper')][1]"
        )
        control_estado.locator(".ts-control").click()
        control_estado.locator(".ts-dropdown").get_by_role(
            "option", name=re.compile(re.escape(estado), re.IGNORECASE)
        ).click()
        self.aplicar_filtro()

    def aplicar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def limpiar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Limpiar")).click()

    def editar(self, nombre):
        self._abrir_edicion(nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()
        self.page.wait_for_url("**/inventario/productos/index", timeout=60_000)

    def cancelar_edicion(self, nombre):
        self._abrir_edicion(nombre)
        self.page.get_by_role("link", name=re.compile("Cancelar")).click()
        self.page.wait_for_url("**/inventario/productos/index")

    def volver_desde_edicion(self, nombre):
        self._abrir_edicion(nombre)
        self.page.get_by_role("link", name=re.compile("Volver")).click()
        self.page.wait_for_url("**/inventario/productos/index")

    def cancelar_eliminacion(self, nombre):
        self._abrir_eliminacion(nombre)
        self.page.get_by_role("button", name="Cancelar").click()

    def eliminar(self, nombre):
        self._abrir_eliminacion(nombre)
        self.page.get_by_role("button", name="Sí, eliminar").click()

    def reactivar(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-activate-")).click()
        self.page.get_by_role("button", name="Sí, activar").click()

    def producto(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_importar(self):
        return self.page.get_by_role("button", name=re.compile("IMPORTAR"))

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("NUEVO", re.IGNORECASE))

    def modal(self):
        return self.page.get_by_role("dialog")

    def modal_activo(self):
        return self.page.locator(".modal.show")

    def formulario_producto(self):
        return self.page.locator("#product-name")

    def opcion_categoria(self, nombre):
        return self.page.get_by_test_id("product-category").get_by_role(
            "option", name=nombre, exact=True
        )

    def categoria_seleccionada(self):
        return self.page.locator("#product-category-ts-control").locator("..").locator(".item")

    def opcion_marca(self, nombre):
        return self.page.get_by_role("option", name=nombre, exact=True)

    def primer_producto_nombre(self):
        return self.page.locator("tbody tr").first.locator("td").nth(1).inner_text()

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def _fila(self, nombre):
        return self.page.locator("tr").filter(
            has_text=re.compile(re.escape(nombre), re.IGNORECASE)
        )

    def _abrir_eliminacion(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-delete-")).click()

    def _abrir_creacion(self):
        self.page.get_by_role("link", name=re.compile("NUEVO", re.IGNORECASE)).click()
        self.page.wait_for_url("**/inventario/productos/crear")

    def _abrir_edicion(self, nombre):
        fila = self._fila(nombre)
        fila.get_by_test_id(re.compile("row-actions-")).click()
        fila.get_by_test_id(re.compile("btn-edit-")).click()
        self.page.wait_for_url("**/inventario/productos/editar/**")

    def _abrir_registro_rapido(self, tipo):
        indice = 0 if tipo == "Categor" else 1
        self.page.get_by_role("button", name=re.compile("Nueva")).nth(indice).click()
        return self.page.get_by_role("dialog").filter(has_text=re.compile(tipo))
