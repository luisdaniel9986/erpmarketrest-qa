import re

import pytest
from playwright.sync_api import Page, expect

from pages.sale.comprobante_venta_page import ComprobanteVentaPage
from pages.login_page import LoginPage


@pytest.fixture
def comprobante_venta_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ComprobanteVentaPage(page)
    modulo.ir_a_comprobantes_venta()
    return modulo


def test_listado_y_filtro_de_comprobantes(comprobante_venta_page: ComprobanteVentaPage):
    comprobante_venta_page.aplicar_filtro()
    expect(comprobante_venta_page.page.locator("table.table-hover")).to_be_visible()


def test_agregar_producto_al_carrito_actualiza_total(
    comprobante_venta_page: ComprobanteVentaPage,
):
    # Test de humo de la pantalla de creación (carrito, totales): NUNCA
    # completa la venta (no se toca "Cobrar" ni el offcanvas de pago), para
    # no registrar comprobantes reales / no tocar SUNAT.
    if not comprobante_venta_page.puede_vender():
        pytest.skip("La caja no está abierta para el usuario de prueba — no se puede vender.")

    comprobante_venta_page.abrir_creacion()
    expect(comprobante_venta_page.page).to_have_url(re.compile(r"/ventas/ventas/create"))

    expect(comprobante_venta_page.primera_tarjeta_producto()).to_be_visible(timeout=15000)
    comprobante_venta_page.agregar_primer_producto_al_carrito()

    expect(comprobante_venta_page.total_venta()).not_to_have_text("0.00")
