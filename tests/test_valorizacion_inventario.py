import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.valorizacion_inventario_page import ValorizacionInventarioPage


@pytest.fixture
def valorizacion_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = ValorizacionInventarioPage(page)
    modulo.ir_a_valorizacion()
    return modulo


def test_seleccionar_almacen(valorizacion_page):
    expect(valorizacion_page.selector_almacen()).to_be_visible(timeout=60_000)
    valorizacion_page.seleccionar_almacen("CENTRAL")
    expect(valorizacion_page.selector_almacen()).to_have_value(re.compile(r".+"))


def test_exportar_excel_valorizacion(valorizacion_page):
    descarga = valorizacion_page.exportar_excel()
    assert descarga.suggested_filename


def test_abrir_pdf_valorizacion(valorizacion_page):
    pdf = valorizacion_page.abrir_pdf()
    assert not pdf.is_closed()


def test_buscar_en_tabla_valorizacion(valorizacion_page):
    texto_original = valorizacion_page.texto_primera_fila()
    buscador = valorizacion_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(valorizacion_page.page.locator("tbody")).not_to_contain_text(texto_original)
    buscador.clear()
