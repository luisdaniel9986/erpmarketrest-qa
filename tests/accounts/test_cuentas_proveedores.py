import re

import pytest
from playwright.sync_api import Page, expect

from pages.accounts.cuentas_proveedores_page import CuentasProveedoresPage
from pages.login_page import LoginPage


@pytest.fixture
def cuentas_proveedores_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = CuentasProveedoresPage(page)
    modulo.ir_a_cuentas_proveedores()
    return modulo


def test_cuentas_por_pagar_visible(cuentas_proveedores_page: CuentasProveedoresPage):
    expect(cuentas_proveedores_page.titulo()).to_be_visible()
    expect(cuentas_proveedores_page.boton_pagar_seleccionadas()).to_be_visible()


def test_filtrar_por_estado_pendiente(cuentas_proveedores_page: CuentasProveedoresPage):
    cuentas_proveedores_page.filtrar_por_estado("Pendiente")
    cuentas_proveedores_page.filtrar()
    expect(cuentas_proveedores_page.titulo()).to_be_visible()
