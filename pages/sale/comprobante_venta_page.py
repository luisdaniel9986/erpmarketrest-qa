
import re

from playwright.sync_api import expect


class ComprobanteVentaPage:
    def __init__(self, page):
        self.page = page

    # Navegación
    def ir_a_comprobantes_venta(self):
        self.page.get_by_role(
            "button", name=re.compile("Ventas")
        ).click()

        self.page.get_by_role(
            "link", name="Comprobante Venta", exact=True
        ).click()

    def aplicar_filtro(self):
        self.page.get_by_role(
            "button", name=re.compile("Filtrar")
        ).click()

    def boton_nuevo(self):
        return self.page.get_by_role(
            "button", name=re.compile("NUEVO")
        )

    def puede_vender(self):
        return self.boton_nuevo().is_enabled()

    def abrir_creacion(self):
        with self.page.expect_navigation():
            self.boton_nuevo().click()

    # Productos y caja
    def seleccionar_caja(self):
        self.page.get_by_role(
            "button", name="834"
        ).click()

    def agregar_productos_grabados(self):
        selectores = [
            "div:nth-child(10) > .card > .pc-img-wrap > .pc-add-btn",
            "div:nth-child(8) > .card > .pc-img-wrap > .pc-add-btn",
            "div:nth-child(4) > .card > .pc-img-wrap > .pc-add-btn",
        ]

        for selector in selectores:
            self.page.locator(selector).click()

    def primera_tarjeta_producto(self):
        return self.page.locator(".product-card").first

    def agregar_primer_producto_al_carrito(self):
        self.primera_tarjeta_producto().click()

    def total_venta(self):
        return self.page.locator(
            ".payment__total .total-amount"
        )

    def subtotal_venta(self):
        return self.page.locator(
            ".rt-row .rt-value"
        ).first

    def buscador_producto(self):
        return self.page.get_by_test_id(
            "sale-product-search"
        )

    # Tipo de comprobante y cliente
    def seleccionar_tipo_boleta(self):
        self.page.locator(
            "#form-store"
        ).get_by_text("B", exact=True).click()

    def seleccionar_cliente_por_documento(self, fragmento_documento):
        control = self.page.locator(
            "#sale_customer_id-ts-control"
        )
        control.fill(fragmento_documento)

        opcion = self.page.get_by_role(
            "option",
            name=re.compile("ALVA LUJAN, LUIS DANIEL DNI:", re.IGNORECASE),
        )
        opcion.click()

    # Cobro
    def abrir_cobro(self):
        self.page.locator("button.payment__total").click()

    def seleccionar_boleta_en_cobro(self):
        self.page.get_by_role(
            "button",
            name=re.compile("B BOLETA DE VENTA ELECTRÓ"),
        ).click()

    def seleccionar_medio_pago(self, medio="MIXTO"):
        control = self.page.locator(
            '[data-testid="off-sale-payment-method"] .ts-control'
        )

        control.scroll_into_view_if_needed()
        control.click()

        opcion = self.page.locator(
            "#off-sale-payment-method-ts-dropdown "
            "[role='option']"
        ).filter(has_text=medio)

        opcion.click()

    def importe_pago(self, numero):
        return self.page.get_by_test_id(
            f"off-sale-pay-amount-{numero}"
        )

    def observaciones(self):
        return self.page.get_by_role(
            "textbox", name="Observaciones"
        )

    def confirmar_grabacion(self):
        with self.page.expect_popup() as popup_info:
            self.page.get_by_role(
                "button", name="Sí!"
            ).click()

        popup = popup_info.value
        popup.wait_for_load_state()
        popup.close()

    def grabar_venta(self, observacion):
        self.observaciones().fill(observacion)
        self.page.get_by_role(
            "button", name="Grabar Venta"
        ).click()
        self.confirmar_grabacion()

        # Esperar el retorno al index
        self.page.wait_for_url(
            "**/ventas/ventas/index",
            timeout=15000
        )

        # Esperar a que aparezca la tabla
        self.tabla_comprobantes().wait_for(
            state="visible",
            timeout=15000
        )

    # Comprobante generado
    def fila_por_observacion(self, observacion):
        return self.page.locator("tr").filter(
            has_text=observacion
        )

    def enviar_fila_a_sunat(self):
        fila = self.page.locator("table tbody tr").first

        # Abrir el dropdown de acciones de la fila
        fila.locator(
            "button[data-testid^='row-actions-']"
        ).click()

        # Localizar la opción Sunat dentro de esa fila
        opcion_sunat = fila.locator(
            "a.btnSendSunat"
        )
        opcion_sunat.click()

        # Confirmar el envío
        self.page.get_by_role(
            "button",
            name="Sí, enviar!"
        ).click()

    def visualizar_pdf_ultimo_comprobante(self):
        # Esperar a que la tabla tenga filas
        filas = self.page.locator("table tbody tr")
        expect(filas.first).to_be_visible()

        # La última fila del DataTable contiene el último registro
        fila = filas.last

        # Verificar que SUNAT lo haya aceptado
        expect(
            fila.get_by_text("ACEPTADO", exact=True)
        ).to_be_visible(timeout=15000)

        # Obtener el enlace PDF de esa fila
        enlace_pdf = fila.get_by_role("link", name="PDF")
        expect(enlace_pdf).to_be_visible()

        # Abrir el PDF en una nueva pestaña
        with self.page.expect_popup() as nueva_pestana:
            enlace_pdf.click()

        pagina_pdf = nueva_pestana.value
        pagina_pdf.wait_for_load_state("domcontentloaded")

        # Mantener el PDF visible durante 15 segundos para el video
        pagina_pdf.wait_for_timeout(15000)

        return pagina_pdf

    def tabla_comprobantes(self):
        return self.page.locator("table.table-hover")
