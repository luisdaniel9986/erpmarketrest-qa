import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.purchases.proveedor_page import ProveedorPage
from pages.login_page import LoginPage


@pytest.fixture
def proveedor_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ProveedorPage(page)
    modulo.ir_a_proveedores()
    return modulo


def _ruc_unico():
    return "20" + str(int(time.time()))[-9:]


def test_crear_proveedor(proveedor_page: ProveedorPage):
    nombre = f"PROVEEDOR QA {int(time.time())}"

    proveedor_page.crear_proveedor(nombre, _ruc_unico())
    expect(proveedor_page.proveedor(nombre)).to_be_visible()

    proveedor_page.eliminar_proveedor(nombre)
    expect(proveedor_page.proveedor(nombre)).to_be_hidden()


def test_cancelar_creacion_vuelve_al_listado(proveedor_page: ProveedorPage):
    proveedor_page.ir_a_crear()
    proveedor_page.volver()
    expect(proveedor_page.boton_nuevo()).to_be_visible()


def test_consultar_documento_no_rompe_el_formulario(proveedor_page: ProveedorPage):
    proveedor_page.ir_a_crear()
    proveedor_page.campo_nro_documento().fill(_ruc_unico())
    proveedor_page.consultar_documento()
    expect(proveedor_page.campo_nombre()).to_be_visible()


def test_editar_proveedor(proveedor_page: ProveedorPage):
    timestamp = int(time.time())
    nombre_inicial = f"PROVEEDOR TEMP {timestamp}"
    nombre_editado = f"PROVEEDOR EDIT {timestamp}"

    proveedor_page.crear_proveedor(nombre_inicial, _ruc_unico())
    proveedor_page.editar_proveedor(nombre_inicial, nombre_editado)

    expect(proveedor_page.proveedor(nombre_editado)).to_be_visible()
    expect(proveedor_page.proveedor(nombre_inicial)).to_be_hidden()

    proveedor_page.eliminar_proveedor(nombre_editado)
    expect(proveedor_page.proveedor(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(proveedor_page: ProveedorPage):
    nombre = f"PROVEEDOR NO_DEL {int(time.time())}"
    proveedor_page.crear_proveedor(nombre, _ruc_unico())

    proveedor_page.cancelar_eliminacion(nombre)
    expect(proveedor_page.proveedor(nombre)).to_be_visible()

    proveedor_page.page.wait_for_timeout(500)

    proveedor_page.eliminar_proveedor(nombre)
    expect(proveedor_page.proveedor(nombre)).to_be_hidden()
