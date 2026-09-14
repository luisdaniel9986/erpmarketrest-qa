import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.colaborador_page import ColaboradorPage


@pytest.fixture
def colaborador_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ColaboradorPage(page)
    modulo.ir_a_colaboradores()
    return modulo


def _dni_unico():
    return f"{int(time.time()) % 100000000:08d}"


def test_crear_y_eliminar_colaborador(colaborador_page: ColaboradorPage):
    nombre = f"COLABORADOR QA {int(time.time())}"

    colaborador_page.crear(nombre, _dni_unico(), "999888777")
    expect(colaborador_page.colaborador(nombre)).to_be_visible()

    colaborador_page.eliminar(nombre)
    expect(colaborador_page.colaborador(nombre)).to_be_hidden()


def test_cancelar_creacion_colaborador(colaborador_page: ColaboradorPage):
    colaborador_page.cancelar_creacion()
    expect(colaborador_page.boton_nuevo()).to_be_visible()
