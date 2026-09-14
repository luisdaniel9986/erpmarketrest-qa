import re


class ComprobanteVentaPage:
    def __init__(self, page):
        self.page = page

    def ir_a_comprobantes_venta(self):
        self.page.get_by_role("button", name=re.compile("Ventas")).click()
        self.page.get_by_role("link", name="Comprobante Venta", exact=True).click()

    def aplicar_filtro(self):
        self.page.get_by_role("button", name=re.compile("Filtrar")).click()

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("NUEVO"))

    def puede_vender(self):
        return self.boton_nuevo().is_enabled()

    def abrir_creacion(self):
        # El botón "NUEVO" valida server-side (checkCanSell) antes de navegar,
        # así que hay que esperar la navegación en vez de solo el click.
        with self.page.expect_navigation():
            self.boton_nuevo().click()

    def primera_tarjeta_producto(self):
        return self.page.locator(".product-card").first

    def agregar_primer_producto_al_carrito(self):
        self.primera_tarjeta_producto().click()

    def total_venta(self):
        return self.page.locator(".payment__total .total-amount")

    def subtotal_venta(self):
        return self.page.locator(".rt-row .rt-value").first

    def buscador_producto(self):
        return self.page.get_by_test_id("sale-product-search")
