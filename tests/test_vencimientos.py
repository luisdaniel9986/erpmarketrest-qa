import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.vencimientos_page import VencimientosPage


@pytest.fixture
def vencimientos_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = VencimientosPage(page)
    modulo.ir_a_vencimientos()
    return modulo


def test_filtrar_y_limpiar_vencimientos(vencimientos_page):
    vencimientos_page.filtrar("CENTRAL", 30)
    vencimientos_page.limpiar()


def test_exportar_excel_vencimientos(vencimientos_page):
    descarga = vencimientos_page.exportar_excel()
    assert descarga.suggested_filename


def test_abrir_pdf_vencimientos(vencimientos_page):
    pdf = vencimientos_page.abrir_pdf()
    assert not pdf.is_closed()


def test_buscar_en_tabla_vencimientos(vencimientos_page):
    buscador = vencimientos_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    buscador.clear()


def test_cancelar_baja(vencimientos_page):
    vencimientos_page.abrir_primera_baja()
    expect(vencimientos_page.cantidad_baja()).to_be_visible()
    vencimientos_page.cancelar_baja()
    expect(vencimientos_page.alerta_baja()).to_be_hidden()


def test_paginacion_vencimientos(vencimientos_page):
    primero = vencimientos_page.boton_paginacion("First")
    anterior = vencimientos_page.boton_paginacion("Previous")
    siguiente = vencimientos_page.boton_paginacion("Next")
    ultimo = vencimientos_page.boton_paginacion("Last")
    for boton in (primero, anterior, siguiente, ultimo):
        expect(boton).to_be_visible()
    expect(primero).to_be_disabled()
    expect(anterior).to_be_disabled()
    if siguiente.is_enabled():
        vencimientos_page.ir_a_pagina("Next")
        expect(anterior).to_be_enabled()
        vencimientos_page.ir_a_pagina("Previous")
        vencimientos_page.ir_a_pagina("Last")
        expect(primero).to_be_enabled()
        vencimientos_page.ir_a_pagina("First")
    else:
        expect(ultimo).to_be_disabled()
