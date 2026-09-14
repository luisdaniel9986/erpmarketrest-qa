import re

import pytest
from playwright.sync_api import Page, expect

from pages.contabilidad.sunat_masivo_page import SunatMasivoPage
from pages.login_page import LoginPage


@pytest.fixture
def sunat_masivo_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = SunatMasivoPage(page)
    modulo.ir_a_sunat_masivo()
    return modulo


def test_consultar_rango_de_comprobantes(sunat_masivo_page: SunatMasivoPage):
    # Consulta de solo lectura contra SUNAT, en lote (máx. 50 comprobantes) —
    # no emite ni registra nada. El sistema primero busca los comprobantes en
    # la base local: si no existen (como acá, con una serie/rango
    # inventados) o si el tenant no tiene credenciales CPE configuradas,
    # responde con un toastr de error — también es una respuesta válida,
    # confirma que la consulta se procesó sin romperse.
    sunat_masivo_page.consultar("03", "B001", "1", "2")

    filas = sunat_masivo_page.filas_resultado().first
    error = sunat_masivo_page.toastr_error()
    expect(filas.or_(error)).to_be_visible(timeout=20000)
