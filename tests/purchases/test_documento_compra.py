import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.purchases.documento_compra_page import DocumentoCompraPage


@pytest.fixture
def documento_compra_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = DocumentoCompraPage(page)
    modulo.ir_a_documento_compra()
    return modulo


def test_crear_y_anular_documento_de_compra(documento_compra_page: DocumentoCompraPage):
    numero = str(int(time.time()))[-6:]
    serie = "F001"

    documento_compra_page.ir_a_crear()
    documento_compra_page.completar_cabecera(serie, numero, "2026-01-15")
    documento_compra_page.agregar_primer_producto()
    documento_compra_page.registrar()

    expect(documento_compra_page.page).to_have_url(re.compile(r"/compras/compras/index"))
    fila = documento_compra_page.fila_por_serie_numero(serie, numero)
    expect(fila).to_be_visible()

    documento_compra_page.anular(serie, numero)
    expect(fila.get_by_text("PENDIENTE")).to_be_hidden()


def test_buscar_documento_de_compra_sin_resultados(documento_compra_page: DocumentoCompraPage):
    buscador = documento_compra_page.buscar("DOCUMENTO_QA_SIN_RESULTADOS_XYZ")
    expect(buscador).to_have_value("DOCUMENTO_QA_SIN_RESULTADOS_XYZ")
    expect(documento_compra_page.page.locator("#table_purchase_documents tbody")).to_contain_text(
        "No se encontraron registros coincidentes"
    )
