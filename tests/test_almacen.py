import re
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from pages.almacen_page import AlmacenPage
from pages.login_page import LoginPage


def nombre_almacen_unico():
    return f"ALMACEN_QA_{uuid4().hex[:8].upper()}"


@pytest.fixture
def almacen_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = AlmacenPage(page)
    modulo.ir_a_almacenes()
    return modulo


def test_crear_almacen(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    expect(almacen_page.almacen(nombre)).to_be_visible()


def test_cancelar_creacion(almacen_page):
    almacen_page.cancelar_creacion()
    expect(almacen_page.modal()).to_be_hidden()
    expect(almacen_page.boton_nuevo()).to_be_visible()


def test_cerrar_creacion_con_x(almacen_page):
    almacen_page.cerrar_creacion()
    expect(almacen_page.modal()).to_be_hidden()
    expect(almacen_page.boton_nuevo()).to_be_visible()


def test_filtrar_almacenes_activos(almacen_page):
    almacen_page.filtrar_por_estado("ACTIVO")
    almacen_page.limpiar_filtro()


def test_ver_detalle(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.ver_detalle(nombre)
    expect(almacen_page.modal()).to_be_visible()
    almacen_page.cerrar_detalle()
    expect(almacen_page.modal()).to_be_hidden()


def test_cerrar_detalle_con_x(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.cerrar_detalle_con_x(nombre)
    expect(almacen_page.modal()).to_be_hidden()


def test_editar_almacen(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.editar(nombre)
    expect(almacen_page.almacen(nombre)).to_be_visible()


def test_cancelar_edicion(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.cancelar_edicion(nombre)
    expect(almacen_page.modal()).to_be_hidden()
    expect(almacen_page.almacen(nombre)).to_be_visible()


def test_cerrar_edicion_con_x(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.cerrar_edicion(nombre)
    expect(almacen_page.modal()).to_be_hidden()
    expect(almacen_page.almacen(nombre)).to_be_visible()


def test_cancelar_eliminacion(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.cancelar_eliminacion(nombre)
    expect(almacen_page.almacen(nombre)).to_be_visible()


def test_eliminar_y_reactivar_almacen(almacen_page):
    nombre = nombre_almacen_unico()
    almacen_page.crear_almacen(nombre, "SEDE CENTRAL")
    almacen_page.eliminar(nombre)
    expect(almacen_page.alerta_de_confirmacion()).to_be_hidden()
    almacen_page.filtrar_por_estado("ANULADO")
    almacen_page.aplicar_filtro()
    expect(almacen_page.almacen(nombre)).to_be_visible()
    almacen_page.reactivar(nombre)
    almacen_page.limpiar_filtro()
    expect(almacen_page.almacen(nombre)).to_be_visible()
