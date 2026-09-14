import re


class CondicionPagoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_condiciones_pago(self):
        self.page.goto("/ventas/condiciones_pago/metodo_pago/index")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("NUEVO")).click()

    def crear_condicion_credito(self, nro_dias):
        self.ir_a_crear()
        self.page.locator("#payment-condition-tipo").select_option("2")
        self.page.locator("#payment-condition-nro-dias").fill(str(nro_dias))
        self.page.get_by_role("button", name=re.compile("REGISTRAR")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, REGISTRAR")).click()
        self.page.wait_for_url(re.compile(r"/condiciones_pago"))

    def editar_condicion(self, nombre_fila, nro_dias):
        fila = self._abrir_opciones(nombre_fila)
        fila.get_by_text("Editar").click()
        self.page.locator("#payment-condition-nro-dias").fill(str(nro_dias))
        self.page.get_by_role("button", name=re.compile("ACTUALIZAR")).click()
        self.page.get_by_role("button", name=re.compile("SÍ, ACTUALIZAR")).click()
        self.page.wait_for_url(re.compile(r"/condiciones_pago"))

    def eliminar_condicion(self, nombre_fila):
        fila = self._abrir_opciones(nombre_fila)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def cancelar_eliminacion(self, nombre_fila):
        fila = self._abrir_opciones(nombre_fila)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("No, cancelar")).click()

    def fila_con_texto(self, texto):
        return self.page.locator("tr").filter(has_text=texto)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("NUEVO"))

    def _abrir_opciones(self, texto):
        fila = self.fila_con_texto(texto)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
