import re

import pytest
from playwright.sync_api import Page, expect

from pages.cashier.mostrador_cajero_page import MostradorCajeroPage
from pages.login_page import LoginPage


@pytest.fixture
def mostrador_cajero_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = MostradorCajeroPage(page)
    modulo.ir_a_mostrador_cajero()
    return modulo


def test_mostrador_cajero_visible(mostrador_cajero_page: MostradorCajeroPage):
    expect(mostrador_cajero_page.titulo()).to_be_visible()
    expect(mostrador_cajero_page.tabla()).to_be_visible()


def test_filtrar_por_estado_finalizado(mostrador_cajero_page: MostradorCajeroPage):
    mostrador_cajero_page.filtrar_por_estado("FINALIZADO")
    mostrador_cajero_page.filtrar()
    expect(mostrador_cajero_page.tabla()).to_be_visible()
