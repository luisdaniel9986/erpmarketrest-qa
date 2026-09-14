import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.supply.tipo_plato_page import TipoPlatoPage
from pages.login_page import LoginPage


@pytest.fixture
def tipo_plato_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = TipoPlatoPage(page)
    modulo.ir_a_tipos_plato()
    return modulo


def test_crear_tipo_plato(tipo_plato_page: TipoPlatoPage):
    nombre = f"TIPO PLATO QA {int(time.time())}"

    tipo_plato_page.crear_tipo_plato(nombre)
    expect(tipo_plato_page.tipo_plato(nombre)).to_be_visible()

    tipo_plato_page.eliminar_tipo_plato(nombre)
    expect(tipo_plato_page.tipo_plato(nombre)).to_be_hidden()


def test_cancelar_creacion(tipo_plato_page: TipoPlatoPage):
    tipo_plato_page.cancelar_creacion()
    expect(tipo_plato_page.boton_nuevo()).to_be_visible()


def test_editar_tipo_plato(tipo_plato_page: TipoPlatoPage):
    timestamp = int(time.time())
    nombre_inicial = f"TIPO TEMP {timestamp}"
    nombre_editado = f"TIPO EDIT {timestamp}"

    tipo_plato_page.crear_tipo_plato(nombre_inicial)
    tipo_plato_page.editar_tipo_plato(nombre_inicial, nombre_editado)

    expect(tipo_plato_page.tipo_plato(nombre_editado)).to_be_visible()
    expect(tipo_plato_page.tipo_plato(nombre_inicial)).to_be_hidden()

    tipo_plato_page.eliminar_tipo_plato(nombre_editado)
    expect(tipo_plato_page.tipo_plato(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(tipo_plato_page: TipoPlatoPage):
    nombre = f"TIPO NO_DEL {int(time.time())}"
    tipo_plato_page.crear_tipo_plato(nombre)

    tipo_plato_page.cancelar_eliminacion(nombre)
    expect(tipo_plato_page.tipo_plato(nombre)).to_be_visible()

    tipo_plato_page.page.wait_for_timeout(500)

    tipo_plato_page.eliminar_tipo_plato(nombre)
    expect(tipo_plato_page.tipo_plato(nombre)).to_be_hidden()
