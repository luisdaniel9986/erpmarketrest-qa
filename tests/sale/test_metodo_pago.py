import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.sale.metodo_pago_page import MetodoPagoPage
from pages.login_page import LoginPage


@pytest.fixture
def metodo_pago_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = MetodoPagoPage(page)
    modulo.ir_a_metodos_pago()
    return modulo


def test_crear_metodo_pago(metodo_pago_page: MetodoPagoPage):
    descripcion = f"METODO QA {int(time.time())}"

    metodo_pago_page.crear_metodo_pago(descripcion)
    expect(metodo_pago_page.metodo_pago(descripcion)).to_be_visible()

    metodo_pago_page.eliminar_metodo_pago(descripcion)
    expect(metodo_pago_page.metodo_pago(descripcion)).to_be_hidden()


def test_cancelar_creacion(metodo_pago_page: MetodoPagoPage):
    metodo_pago_page.cancelar_creacion()
    expect(metodo_pago_page.boton_nuevo()).to_be_visible()


def test_editar_metodo_pago(metodo_pago_page: MetodoPagoPage):
    timestamp = int(time.time())
    descripcion_inicial = f"METODO TEMP {timestamp}"
    descripcion_editada = f"METODO EDIT {timestamp}"

    metodo_pago_page.crear_metodo_pago(descripcion_inicial)
    metodo_pago_page.editar_metodo_pago(descripcion_inicial, descripcion_editada)

    expect(metodo_pago_page.metodo_pago(descripcion_editada)).to_be_visible()
    expect(metodo_pago_page.metodo_pago(descripcion_inicial)).to_be_hidden()

    metodo_pago_page.eliminar_metodo_pago(descripcion_editada)
    expect(metodo_pago_page.metodo_pago(descripcion_editada)).to_be_hidden()


def test_cancelar_eliminacion(metodo_pago_page: MetodoPagoPage):
    descripcion = f"METODO NO_DEL {int(time.time())}"
    metodo_pago_page.crear_metodo_pago(descripcion)

    metodo_pago_page.cancelar_eliminacion(descripcion)
    expect(metodo_pago_page.metodo_pago(descripcion)).to_be_visible()

    metodo_pago_page.page.wait_for_timeout(500)

    metodo_pago_page.eliminar_metodo_pago(descripcion)
    expect(metodo_pago_page.metodo_pago(descripcion)).to_be_hidden()


def test_ir_a_cuentas(metodo_pago_page: MetodoPagoPage):
    descripcion = f"METODO CUENTAS {int(time.time())}"
    metodo_pago_page.crear_metodo_pago(descripcion)

    metodo_pago_page.ir_a_cuentas(descripcion)
    expect(metodo_pago_page.page).to_have_url(re.compile(r"assign-accounts"))

    metodo_pago_page.ir_a_metodos_pago()
    metodo_pago_page.eliminar_metodo_pago(descripcion)
    expect(metodo_pago_page.metodo_pago(descripcion)).to_be_hidden()
