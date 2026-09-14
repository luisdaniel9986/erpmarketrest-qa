import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.orders.mostrador_mesero_page import MostradorMeseroPage


@pytest.fixture
def mostrador_mesero_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = MostradorMeseroPage(page)
    modulo.ir_a_mostrador_mesero()
    return modulo


def test_mostrador_mesero_carga_el_plano_de_mesas(mostrador_mesero_page: MostradorMeseroPage):
    expect(mostrador_mesero_page.titulo()).to_be_visible()


def test_filtros_de_mesas(mostrador_mesero_page: MostradorMeseroPage):
    mostrador_mesero_page.filtrar_libres()
    mostrador_mesero_page.filtrar_todas()
    mostrador_mesero_page.actualizar()
    expect(mostrador_mesero_page.titulo()).to_be_visible()
