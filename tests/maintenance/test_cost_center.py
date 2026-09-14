import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.cost_center_page import CostCenterPage


@pytest.fixture
def cost_center_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = CostCenterPage(page)
    modulo.ir_a_centros_costo()
    return modulo


def test_crear_centro_costo(cost_center_page: CostCenterPage):
    nombre = f"CENTRO COSTO TEST {int(time.time())}"

    cost_center_page.crear_centro_costo(nombre)
    expect(cost_center_page.centro_costo(nombre)).to_be_visible()

    cost_center_page.eliminar_centro_costo(nombre)
    expect(cost_center_page.centro_costo(nombre)).to_be_hidden()


def test_cancelar_creacion(cost_center_page: CostCenterPage):
    cost_center_page.cancelar_creacion()
    expect(cost_center_page.boton_nuevo()).to_be_visible()


def test_buscar_centro_costo(cost_center_page: CostCenterPage):
    nombre = f"CENTRO COSTO BUSCAR {int(time.time())}"
    cost_center_page.crear_centro_costo(nombre)

    cost_center_page.buscar_centro_costo(nombre)
    expect(cost_center_page.centro_costo(nombre)).to_be_visible()

    cost_center_page.eliminar_centro_costo(nombre)


def test_editar_centro_costo(cost_center_page: CostCenterPage):
    timestamp = int(time.time())
    nombre_inicial = f"CENTRO TEMP {timestamp}"
    nombre_editado = f"CENTRO EDIT {timestamp}"

    cost_center_page.crear_centro_costo(nombre_inicial)
    cost_center_page.editar_centro_costo(nombre_inicial, nombre_editado)

    expect(cost_center_page.centro_costo(nombre_editado)).to_be_visible()
    expect(cost_center_page.centro_costo(nombre_inicial)).to_be_hidden()

    cost_center_page.eliminar_centro_costo(nombre_editado)
    expect(cost_center_page.centro_costo(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(cost_center_page: CostCenterPage):
    nombre = f"CENTRO NO_DEL {int(time.time())}"
    cost_center_page.crear_centro_costo(nombre)

    cost_center_page.cancelar_eliminacion(nombre)
    expect(cost_center_page.centro_costo(nombre)).to_be_visible()

    cost_center_page.page.wait_for_timeout(500)

    cost_center_page.eliminar_centro_costo(nombre)
    expect(cost_center_page.centro_costo(nombre)).to_be_hidden()


def test_eliminar_centro_costo(cost_center_page: CostCenterPage):
    nombre = f"CENTRO DEL {int(time.time())}"
    cost_center_page.crear_centro_costo(nombre)

    cost_center_page.eliminar_centro_costo(nombre)
    expect(cost_center_page.alerta_de_confirmacion()).to_be_hidden()
    expect(cost_center_page.centro_costo(nombre)).to_be_hidden()
