import re

import pytest
from playwright.sync_api import Page, expect

from pages.kardex_page import KardexPage
from pages.login_page import LoginPage


@pytest.fixture
def kardex_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = KardexPage(page)
    modulo.ir_a_kardex()
    return modulo


def test_filtrar_y_limpiar_kardex(kardex_page):
    kardex_page.seleccionar_producto()
    kardex_page.filtrar()
    kardex_page.limpiar()


def test_limpiar_producto_con_x(kardex_page):
    kardex_page.seleccionar_producto()
    expect(kardex_page.selector_producto()).to_have_value(re.compile(r".+"))
    kardex_page.limpiar_producto_con_x()
    expect(kardex_page.selector_producto()).to_have_value("")


def test_abrir_pdf_kardex(kardex_page):
    kardex_page.seleccionar_producto()
    kardex_page.filtrar()
    pdf = kardex_page.abrir_pdf()
    assert not pdf.is_closed()


def test_filtrar_por_almacen_y_fechas(kardex_page):
    kardex_page.seleccionar_producto()
    kardex_page.seleccionar_almacen("CENTRAL")
    kardex_page.establecer_fechas("2026-01-01", "2026-12-31")
    kardex_page.filtrar()
    kardex_page.limpiar()


def test_exportar_excel_kardex(kardex_page):
    kardex_page.seleccionar_producto()
    kardex_page.filtrar()
    descarga = kardex_page.exportar_excel()
    assert descarga.suggested_filename


def test_buscar_en_tabla_kardex(kardex_page):
    kardex_page.seleccionar_producto()
    kardex_page.filtrar()
    texto_original = kardex_page.texto_primera_fila()
    buscador = kardex_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(kardex_page.page.locator("tbody")).not_to_contain_text(texto_original)
    buscador.clear()


def test_paginacion_kardex(kardex_page):
    primero = kardex_page.boton_paginacion("First")
    anterior = kardex_page.boton_paginacion("Previous")
    siguiente = kardex_page.boton_paginacion("Next")
    ultimo = kardex_page.boton_paginacion("Last")

    for boton in (primero, anterior, siguiente, ultimo):
        expect(boton).to_be_visible()

    expect(primero).to_be_disabled()
    expect(anterior).to_be_disabled()

    if siguiente.is_enabled():
        kardex_page.ir_a_pagina("Next")
        expect(anterior).to_be_enabled()
        kardex_page.ir_a_pagina("Previous")
        kardex_page.ir_a_pagina("Last")
        expect(primero).to_be_enabled()
        kardex_page.ir_a_pagina("First")
    else:
        expect(ultimo).to_be_disabled()
