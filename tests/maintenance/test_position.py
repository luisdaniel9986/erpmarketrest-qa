import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.position_page import PositionPage


@pytest.fixture
def position_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = PositionPage(page)
    modulo.ir_a_cargos()
    return modulo


def test_crear_cargo(position_page: PositionPage):
    nombre = f"CARGO TEST {int(time.time())}"

    position_page.crear_cargo(nombre)
    expect(position_page.cargo(nombre)).to_be_visible()

    position_page.eliminar_cargo(nombre)
    expect(position_page.cargo(nombre)).to_be_hidden()


def test_cancelar_creacion(position_page: PositionPage):
    position_page.cancelar_creacion()
    expect(position_page.boton_nuevo()).to_be_visible()


def test_buscar_cargo(position_page: PositionPage):
    nombre = f"CARGO BUSCAR {int(time.time())}"
    position_page.crear_cargo(nombre)

    position_page.buscar_cargo(nombre)
    expect(position_page.cargo(nombre)).to_be_visible()

    position_page.eliminar_cargo(nombre)


def test_editar_cargo(position_page: PositionPage):
    timestamp = int(time.time())
    nombre_inicial = f"CARGO TEMP {timestamp}"
    nombre_editado = f"CARGO EDIT {timestamp}"

    position_page.crear_cargo(nombre_inicial)
    position_page.editar_cargo(nombre_inicial, nombre_editado)

    expect(position_page.cargo(nombre_editado)).to_be_visible()
    expect(position_page.cargo(nombre_inicial)).to_be_hidden()

    position_page.eliminar_cargo(nombre_editado)
    expect(position_page.cargo(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(position_page: PositionPage):
    nombre = f"CARGO NO_DEL {int(time.time())}"
    position_page.crear_cargo(nombre)

    position_page.cancelar_eliminacion(nombre)
    expect(position_page.cargo(nombre)).to_be_visible()

    position_page.page.wait_for_timeout(500)

    position_page.eliminar_cargo(nombre)
    expect(position_page.cargo(nombre)).to_be_hidden()


def test_eliminar_cargo(position_page: PositionPage):
    nombre = f"CARGO DEL {int(time.time())}"
    position_page.crear_cargo(nombre)

    position_page.eliminar_cargo(nombre)
    expect(position_page.alerta_de_confirmacion()).to_be_hidden()
    expect(position_page.cargo(nombre)).to_be_hidden()
