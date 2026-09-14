import re

import pytest
from playwright.sync_api import Page, expect

from pages.inventory.kardex_page import KardexPage
from pages.login_page import LoginPage


@pytest.fixture
def kardex_valorizado_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = KardexPage(page, valorizado=True)
    modulo.ir_a_kardex()
    return modulo


def test_filtrar_y_limpiar_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    kardex_valorizado_page.filtrar()
    kardex_valorizado_page.limpiar()


def test_limpiar_producto_con_x_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    expect(kardex_valorizado_page.selector_producto()).to_have_value(re.compile(r".+"))
    kardex_valorizado_page.limpiar_producto_con_x()
    expect(kardex_valorizado_page.selector_producto()).to_have_value("")


def test_abrir_pdf_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    kardex_valorizado_page.filtrar()
    pdf = kardex_valorizado_page.abrir_pdf()
    assert not pdf.is_closed()


def test_filtrar_por_almacen_y_fechas_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    kardex_valorizado_page.seleccionar_almacen("CENTRAL")
    kardex_valorizado_page.establecer_fechas("2026-01-01", "2026-12-31")
    kardex_valorizado_page.filtrar()
    kardex_valorizado_page.limpiar()


def test_exportar_excel_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    kardex_valorizado_page.filtrar()
    descarga = kardex_valorizado_page.exportar_excel()
    assert descarga.suggested_filename


def test_buscar_documento_kardex_valorizado(kardex_valorizado_page):
    kardex_valorizado_page.seleccionar_producto()
    kardex_valorizado_page.filtrar()
    texto_original = kardex_valorizado_page.texto_primera_fila()
    buscador = kardex_valorizado_page.buscar_en_tabla("DOCUMENTO_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("DOCUMENTO_QA_SIN_RESULTADOS")
    expect(kardex_valorizado_page.page.locator("tbody")).not_to_contain_text(
        texto_original
    )
    buscador.clear()
