import re

import pytest
from playwright.sync_api import Page, expect

from pages.inventory.inventario_page import InventarioPage
from pages.login_page import LoginPage


@pytest.fixture
def inventario_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = InventarioPage(page)
    modulo.ir_a_inventario()
    return modulo


def test_filtrar_y_abrir_pdf(inventario_page):
    inventario_page.filtrar(almacen="2", stock="3")
    pdf = inventario_page.abrir_pdf()
    assert not pdf.is_closed()


def test_exportar_excel(inventario_page):
    inventario_page.filtrar(almacen="2", stock="3")
    descarga = inventario_page.exportar_excel()
    assert descarga.suggested_filename


def test_buscar_en_tabla(inventario_page):
    texto_original = inventario_page.texto_primera_fila()
    buscador = inventario_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(inventario_page.page.locator("tbody")).not_to_contain_text(texto_original)
    buscador.clear()
