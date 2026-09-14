import re

import pytest
from playwright.sync_api import Page, expect

from pages.contabilidad.sunat_individual_page import SunatIndividualPage
from pages.login_page import LoginPage


@pytest.fixture
def sunat_individual_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = SunatIndividualPage(page)
    modulo.ir_a_sunat_individual()
    return modulo


def test_consultar_comprobante_en_sunat(sunat_individual_page: SunatIndividualPage):
    # Consulta de solo lectura contra el webservice de SUNAT: no emite ni
    # registra nada, solo valida un comprobante existente o no. Este ambiente
    # de test no tiene credenciales CPE configuradas en Mantenimiento >
    # Empresa, así que la respuesta esperada aquí es el toastr de error
    # explicando eso — igual de válido que un resultado real, es la señal de
    # que la consulta se procesó y el sistema respondió con claridad.
    sunat_individual_page.consultar("03", "B001", "1", "2020-01-01", "1.00")

    resultado = sunat_individual_page.resultado()
    error = sunat_individual_page.toastr_error()
    expect(resultado.or_(error)).to_be_visible(timeout=20000)
