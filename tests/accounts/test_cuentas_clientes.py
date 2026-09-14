import re

import pytest
from playwright.sync_api import Page, expect

from pages.accounts.cuentas_clientes_page import CuentasClientesPage
from pages.login_page import LoginPage


@pytest.fixture
def cuentas_clientes_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = CuentasClientesPage(page)
    modulo.ir_a_cuentas_clientes()
    return modulo


def test_cuentas_por_cobrar_visible(cuentas_clientes_page: CuentasClientesPage):
    expect(cuentas_clientes_page.titulo()).to_be_visible()
    expect(cuentas_clientes_page.boton_pagar_seleccionadas()).to_be_visible()


def test_filtrar_por_estado_pendiente(cuentas_clientes_page: CuentasClientesPage):
    cuentas_clientes_page.filtrar_por_estado("Pendiente")
    cuentas_clientes_page.filtrar()
    expect(cuentas_clientes_page.titulo()).to_be_visible()
