import re


class EgresosPage:
    def __init__(self, page):
        self.page = page

    def ir_a_egresos(self):
        self.page.goto("/cajas/egresos/index")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("NUEVO")).click()
        self.page.wait_for_url(re.compile(r"/cajas/egresos/create"))

    def _elegir_tomselect(self, testid, texto=None):
        combo = self.page.get_by_test_id(testid)
        combo.click()
        opciones = combo.locator(".ts-dropdown .option")
        if texto:
            opciones.filter(has_text=texto).first.click()
        else:
            opciones.first.click()

    def crear_centro_costo_rapido(self, nombre):
        """El ambiente de test puede no tener centros de costo cargados; el
        propio formulario ofrece un '+' para crearlo sin salir de la
        pantalla — lo usamos en vez de depender de datos preexistentes."""
        self.page.get_by_test_id("btn-new-cost-center").click()
        modal = self.page.locator("#mdl-create-cost-center")
        modal.locator("#create-cost-center-name").fill(nombre)
        modal.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name="Sí").click()
        seleccionado = self.page.get_by_test_id("exit-money-cost-center-select").locator(".item")
        seleccionado.wait_for(state="visible", timeout=10_000)

    def completar_egreso(self, numero, descripcion, total, centro_costo=None):
        self.page.get_by_label("Número").fill(numero)
        # El proveedor puede venir precargado (proveedor por defecto del
        # tenant); el combo busca por texto vía API, así que solo lo tocamos
        # si llegó vacío.
        proveedor = self.page.get_by_test_id("exit-money-supplier-select")
        if proveedor.locator(".item").count() == 0:
            proveedor.locator("input").fill("a")
            proveedor.locator(".ts-dropdown .option").first.click(timeout=10_000)

        centro_costo_select = self.page.get_by_test_id("exit-money-cost-center-select")
        if centro_costo_select.locator(".item").count() == 0:
            self.crear_centro_costo_rapido(centro_costo or f"CC QA {numero}")

        self.page.locator('[data-testid^="exit-money-description-"]').first.fill(descripcion)
        self.page.locator('[data-testid^="exit-money-total-"]').first.fill(str(total))

    def guardar(self):
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí, registrar").click()

    def fila_por_numero(self, numero):
        return self.page.locator("tr").filter(has_text=numero)

    def abrir_opciones(self, numero):
        fila = self.fila_por_numero(numero)
        boton = fila.get_by_test_id(re.compile("row-actions-"))
        boton.wait_for(state="visible")
        boton.click()
        return fila

    def anular(self, numero):
        fila = self.abrir_opciones(numero)
        fila.get_by_text("Anular").click()
        self.page.get_by_role("button", name="Sí, anular").click()

    def buscar(self, texto):
        buscador = self.page.locator("#dt-search-0")
        buscador.fill(texto)
        return buscador
