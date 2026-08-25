import re
from pathlib import Path
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.marca_page import MarcaPage


def nombre_marca_unico():
    return f"MARCA_QA_{uuid4().hex[:8].upper()}"


@pytest.fixture
def marca_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = MarcaPage(page)
    modulo.ir_a_marcas()
    return modulo


def test_importar_marcas(marca_page):
    ruta = Path(__file__).parents[1] / "datos" / "formato_import_marcas.xlsx"
    marca_page.importar_marcas(ruta)
    expect(marca_page.boton_importar()).to_be_visible()


def test_cancelar_importacion(marca_page):
    marca_page.cancelar_importacion()
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.boton_importar()).to_be_visible()


def test_cerrar_importacion_con_x(marca_page):
    marca_page.cerrar_importacion()
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.boton_importar()).to_be_visible()


def test_crear_marca(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    expect(marca_page.marca(nombre)).to_be_visible()


def test_cancelar_creacion(marca_page):
    marca_page.cancelar_creacion()
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.boton_nuevo()).to_be_visible()


def test_cerrar_creacion_con_x(marca_page):
    marca_page.cerrar_creacion()
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.boton_nuevo()).to_be_visible()


def test_filtrar_marcas_activas(marca_page):
    marca_page.filtrar_por_estado("ACTIVO")
    marca_page.limpiar_filtro()


def test_editar_marca(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    marca_page.editar(nombre)
    expect(marca_page.marca(nombre)).to_be_visible()


def test_cancelar_edicion(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    marca_page.cancelar_edicion(nombre)
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.marca(nombre)).to_be_visible()


def test_cerrar_edicion_con_x(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    marca_page.cerrar_edicion(nombre)
    expect(marca_page.modal()).to_be_hidden()
    expect(marca_page.marca(nombre)).to_be_visible()


def test_cancelar_eliminacion(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    marca_page.cancelar_eliminacion(nombre)
    expect(marca_page.marca(nombre)).to_be_visible()


def test_eliminar_y_reactivar_marca(marca_page):
    nombre = nombre_marca_unico()
    marca_page.crear(nombre)
    marca_page.eliminar(nombre)
    expect(marca_page.alerta_de_confirmacion()).to_be_hidden()
    marca_page.filtrar_por_estado("ANULADO")
    marca_page.aplicar_filtro()
    expect(marca_page.marca(nombre)).to_be_visible()
    marca_page.reactivar(nombre)
    marca_page.limpiar_filtro()
    expect(marca_page.marca(nombre)).to_be_visible()
