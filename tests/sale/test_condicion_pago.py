import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.sale.condicion_pago_page import CondicionPagoPage
from pages.login_page import LoginPage


@pytest.fixture
def condicion_pago_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = CondicionPagoPage(page)
    modulo.ir_a_condiciones_pago()
    return modulo


def _nro_dias_unico():
    # dias unicos entre 100 y 9999 derivados del timestamp, para poder ubicar la fila creada
    return 100 + (int(time.time()) % 9899)


def test_crear_condicion_credito(condicion_pago_page: CondicionPagoPage):
    nro_dias = _nro_dias_unico()

    condicion_pago_page.crear_condicion_credito(nro_dias)
    expect(condicion_pago_page.fila_con_texto(str(nro_dias))).to_be_visible()

    condicion_pago_page.eliminar_condicion(str(nro_dias))
    expect(condicion_pago_page.fila_con_texto(str(nro_dias))).to_be_hidden()


def test_cancelar_creacion_vuelve_al_listado(condicion_pago_page: CondicionPagoPage):
    condicion_pago_page.ir_a_crear()
    condicion_pago_page.page.get_by_role("link", name=re.compile("VOLVER")).click()
    expect(condicion_pago_page.boton_nuevo()).to_be_visible()


def test_editar_condicion(condicion_pago_page: CondicionPagoPage):
    nro_dias_inicial = _nro_dias_unico()
    nro_dias_editado = nro_dias_inicial + 1

    condicion_pago_page.crear_condicion_credito(nro_dias_inicial)
    condicion_pago_page.editar_condicion(str(nro_dias_inicial), nro_dias_editado)

    expect(condicion_pago_page.fila_con_texto(str(nro_dias_editado))).to_be_visible()

    condicion_pago_page.eliminar_condicion(str(nro_dias_editado))
    expect(condicion_pago_page.fila_con_texto(str(nro_dias_editado))).to_be_hidden()


def test_cancelar_eliminacion(condicion_pago_page: CondicionPagoPage):
    nro_dias = _nro_dias_unico()
    condicion_pago_page.crear_condicion_credito(nro_dias)

    condicion_pago_page.cancelar_eliminacion(str(nro_dias))
    expect(condicion_pago_page.fila_con_texto(str(nro_dias))).to_be_visible()

    condicion_pago_page.page.wait_for_timeout(500)

    condicion_pago_page.eliminar_condicion(str(nro_dias))
    expect(condicion_pago_page.fila_con_texto(str(nro_dias))).to_be_hidden()
