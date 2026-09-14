import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.cash.caja_page import CajaPage
from pages.login_page import LoginPage


@pytest.fixture
def caja_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    caja_page = CajaPage(page)
    caja_page.ir_a_cajas()
    return caja_page


def test_crear_caja(caja_page: CajaPage):
    nombre = f"CAJA TEST {int(time.time())}"
    
    caja_page.crear_caja(nombre)
    expect(caja_page.caja(nombre)).to_be_visible()

    caja_page.eliminar_caja(nombre)
    expect(caja_page.caja(nombre)).to_be_hidden()


def test_cancelar_creacion(caja_page: CajaPage):
    caja_page.cancelar_creacion()
    expect(caja_page.boton_nuevo()).to_be_visible()


def test_buscar_caja(caja_page: CajaPage):
    nombre = "CAJA PRINCIPAL"
    caja_page.buscar_caja(nombre)
    expect(caja_page.caja(nombre)).to_be_visible()


def test_editar_caja(caja_page: CajaPage):
    timestamp = int(time.time())
    nombre_inicial = f"CAJA TEMP {timestamp}"
    nombre_editado = f"CAJA EDIT {timestamp}"

    caja_page.crear_caja(nombre_inicial)
    caja_page.editar_caja(nombre_inicial, nombre_editado)

    expect(caja_page.caja(nombre_editado)).to_be_visible()
    expect(caja_page.caja(nombre_inicial)).to_be_hidden()

    caja_page.eliminar_caja(nombre_editado)
    expect(caja_page.caja(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(caja_page: CajaPage):
    nombre = f"CAJA NO_DEL {int(time.time())}"
    caja_page.crear_caja(nombre)
    
    caja_page.cancelar_eliminacion(nombre)
    expect(caja_page.caja(nombre)).to_be_visible()

    caja_page.page.wait_for_timeout(500)

    caja_page.eliminar_caja(nombre)
    expect(caja_page.caja(nombre)).to_be_hidden()


def test_eliminar_caja(caja_page: CajaPage):
    nombre = f"CAJA DEL {int(time.time())}"
    caja_page.crear_caja(nombre)
    
    caja_page.eliminar_caja(nombre)
    expect(caja_page.alerta_de_confirmacion()).to_be_hidden()
    expect(caja_page.caja(nombre)).to_be_hidden()