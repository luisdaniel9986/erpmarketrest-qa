
import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.sale.comprobante_venta_page import ComprobanteVentaPage


@pytest.fixture
def comprobante_venta_page(page: Page, credenciales_cajero):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(
        credenciales_cajero["email"],
        credenciales_cajero["password"],
    )

    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ComprobanteVentaPage(page)
    modulo.ir_a_comprobantes_venta()
    return modulo


def test_listado_y_filtro_de_comprobantes(
    comprobante_venta_page: ComprobanteVentaPage,
):
    comprobante_venta_page.aplicar_filtro()

    expect(
        comprobante_venta_page.tabla_comprobantes()
    ).to_be_visible()


def test_agregar_producto_al_carrito_actualiza_total(
    comprobante_venta_page: ComprobanteVentaPage,
):
    modulo = comprobante_venta_page

    if not modulo.puede_vender():
        pytest.skip(
            "La caja no está abierta o el usuario no puede vender."
        )

    modulo.abrir_creacion()

    expect(modulo.page).to_have_url(
        re.compile(r"/ventas/ventas/create")
    )

    expect(
        modulo.primera_tarjeta_producto()
    ).to_be_visible(timeout=15000)

    modulo.agregar_primer_producto_al_carrito()

    expect(
        modulo.total_venta()
    ).not_to_have_text("0.00")


def test_venta_al_contado_y_envio_sunat(
    comprobante_venta_page: ComprobanteVentaPage,
):
    modulo = comprobante_venta_page

    if not modulo.puede_vender():
        pytest.skip(
            "La caja no está abierta o el usuario no puede vender."
        )

    # 1. Abrir formulario de venta
    modulo.abrir_creacion()

    expect(modulo.page).to_have_url(
        re.compile(r"/ventas/ventas/create")
    )

    # 2. Seleccionar caja y agregar productos
    modulo.seleccionar_caja()
    modulo.agregar_productos_grabados()

    expect(
        modulo.total_venta()
    ).not_to_have_text("0.00")

    # 3. Seleccionar boleta y cliente de prueba
    modulo.seleccionar_tipo_boleta()

    # Usa aquí un cliente autorizado para QA.
    # El selector de cliente debe coincidir con el nombre de tu catálogo.
    modulo.seleccionar_cliente_por_documento("7560")

    # 4. Abrir cobro y elegir boleta
    modulo.abrir_cobro()
    modulo.seleccionar_boleta_en_cobro()

    # 5. Configurar el pago según tu grabación.
    # Tu grabación seleccionó MIXTO con dos importes.
    # Comprueba que ambos importes sumen exactamente el total
    # mostrado por el sistema antes de grabar.
    modulo.seleccionar_medio_pago("MIXTO")
    modulo.importe_pago(1).fill("420")
    modulo.importe_pago(3).fill("25.50")

    observacion = "QA venta contado teclados importacion"

    # 6. Grabar la venta
    modulo.grabar_venta(observacion)

    # 7. Enviar a SUNAT el comprobante de esta venta
    modulo.enviar_fila_a_sunat()

    modulo.visualizar_pdf_ultimo_comprobante()

    # 8. Verificar que se mantiene visible el listado
    expect(
        modulo.tabla_comprobantes()
    ).to_be_visible()
