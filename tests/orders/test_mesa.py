import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.orders.mesa_page import MesaPage
from pages.login_page import LoginPage


@pytest.fixture
def mesa_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = MesaPage(page)
    modulo.ir_a_mesas()
    return modulo


def test_crear_mesa(mesa_page: MesaPage):
    nombre = f"MESA QA {int(time.time())}"

    mesa_page.crear_mesa(nombre)
    expect(mesa_page.mesa(nombre)).to_be_visible()

    mesa_page.eliminar_mesa(nombre)
    expect(mesa_page.mesa(nombre)).to_be_hidden()


def test_cancelar_creacion(mesa_page: MesaPage):
    mesa_page.cancelar_creacion()
    expect(mesa_page.boton_nuevo()).to_be_visible()


def test_editar_mesa(mesa_page: MesaPage):
    timestamp = int(time.time())
    nombre_inicial = f"MESA TEMP {timestamp}"
    nombre_editado = f"MESA EDIT {timestamp}"

    mesa_page.crear_mesa(nombre_inicial)
    mesa_page.editar_mesa(nombre_inicial, nombre_editado)

    expect(mesa_page.mesa(nombre_editado)).to_be_visible()
    expect(mesa_page.mesa(nombre_inicial)).to_be_hidden()

    mesa_page.eliminar_mesa(nombre_editado)
    expect(mesa_page.mesa(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(mesa_page: MesaPage):
    nombre = f"MESA NO_DEL {int(time.time())}"
    mesa_page.crear_mesa(nombre)

    mesa_page.cancelar_eliminacion(nombre)
    expect(mesa_page.mesa(nombre)).to_be_visible()

    mesa_page.page.wait_for_timeout(500)

    mesa_page.eliminar_mesa(nombre)
    expect(mesa_page.mesa(nombre)).to_be_hidden()
