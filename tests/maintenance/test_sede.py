import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.sede_page import SedePage


@pytest.fixture
def sede_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = SedePage(page)
    modulo.ir_a_sedes()
    return modulo


def test_crear_y_eliminar_sede(sede_page: SedePage):
    nombre = f"SEDE QA {int(time.time())}"

    sede_page.crear(nombre)
    expect(sede_page.sede(nombre)).to_be_visible()

    sede_page.eliminar(nombre)
    expect(sede_page.sede(nombre)).to_be_hidden()


def test_cancelar_creacion_sede(sede_page: SedePage):
    sede_page.cancelar_creacion()
    expect(sede_page.boton_nuevo()).to_be_visible()
