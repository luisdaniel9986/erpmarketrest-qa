import re


class DocumentoCompraPage:
    def __init__(self, page):
        self.page = page

    def ir_a_documento_compra(self):
        self.page.goto("/compras/compras/index")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("Nuevo")).click()

    def _elegir_tomselect(self, testid, texto=None):
        combo = self.page.get_by_test_id(testid)
        combo.click()
        opciones = combo.locator(".ts-dropdown .option")
        opcion = opciones.filter(has_text=texto).first if texto else opciones.first
        try:
            opcion.wait_for(state="visible", timeout=2_000)
        except Exception:
            # El clic anterior a veces solo cierra el combo previo en vez de
            # abrir este (le "roba" el foco) — un segundo clic lo abre bien.
            combo.click()
            opcion.wait_for(state="visible", timeout=10_000)
        opcion.click()

    def completar_cabecera(self, serie, numero, fecha_entrega, fecha_vencimiento=None):
        # Tipo Doc ya viene preseleccionado en FACTURA (TomSelect.setValue en
        # el mount del formulario) — no hace falta tocarlo.
        self.page.locator("#purchase-doc-serie").fill(serie)
        self.page.locator("#purchase-doc-numero").fill(numero)
        self.page.locator("#purchase-doc-fecha-entrega").fill(fecha_entrega)
        self.page.locator("#purchase-doc-expiration-date").fill(fecha_vencimiento or fecha_entrega)
        self._elegir_tomselect("purchase-doc-proveedor")
        # Condición CRÉDITO evita por completo "Descontar Caja" (no aplica
        # en crédito — el pago se registra después en Cuentas por
        # Proveedor), así el test no depende de tener una caja abierta.
        self._elegir_tomselect("purchase-doc-payment-condition", texto="CR")
        self._elegir_tomselect("purchase-doc-warehouse")
        self._elegir_tomselect("purchase-doc-cost-center")

    def agregar_primer_producto(self):
        boton = self.page.get_by_role("button", name=re.compile("Buscar Producto"))
        # El primer clic justo después de elegir un TomSelect a veces solo
        # cierra el combo (roba el foco) en vez de llegar al botón — si el
        # modal no abrió a la primera, reintentamos.
        boton.click()
        modal = self.page.locator("#mdlProducts")
        try:
            modal.wait_for(state="visible", timeout=3_000)
        except Exception:
            boton.click()
            modal.wait_for(state="visible", timeout=10_000)
        fila = self.page.locator("#tbl_products_modal tbody tr").first
        fila.wait_for(state="visible")
        fila.click()
        self.page.locator('[data-testid^="purchase-quantity-"]').first.wait_for(state="visible")
        self._completar_vencimiento_si_aplica()

    def _completar_vencimiento_si_aplica(self, fecha="2027-01-01", lote="LOTE-QA"):
        vencimiento = self.page.locator('[data-testid^="purchase-expiration-"]').first
        if vencimiento.count() > 0 and vencimiento.is_visible():
            vencimiento.fill(fecha)
            self.page.locator('[data-testid^="purchase-lot-"]').first.fill(lote)

    def registrar(self):
        boton = self.page.get_by_role("button", name=re.compile("Registrar")).first
        swal = self.page.locator(".swal2-popup")
        boton.click()
        try:
            swal.wait_for(state="visible", timeout=3_000)
        except Exception:
            boton.click()
            swal.wait_for(state="visible", timeout=10_000)
        self.page.get_by_role("button", name="Sí, registrar").click()

    def fila_por_serie_numero(self, serie, numero):
        return self.page.locator("tr").filter(has_text=f"{serie}-{numero}")

    def abrir_opciones(self, serie, numero):
        fila = self.fila_por_serie_numero(serie, numero)
        boton = fila.get_by_test_id(re.compile("row-actions-"))
        boton.wait_for(state="visible")
        boton.click()
        return fila

    def anular(self, serie, numero):
        fila = self.abrir_opciones(serie, numero)
        fila.get_by_text("Anular").click()
        self.page.get_by_role("button", name="Sí, anular").click()

    def buscar(self, texto):
        buscador = self.page.locator('input[aria-controls="table_purchase_documents"]')
        buscador.fill(texto)
        return buscador
