import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.supply.plato_page import PlatoPage
from pages.supply.tipo_plato_page import TipoPlatoPage
from pages.login_page import LoginPage


def _borrar_tipo_plato_creado(page, tipo):
    """crear_plato() siempre da de alta un Tipo de Plato nuevo (vía '+
    Nuevo' dentro del formulario) y nada lo borra en cascada al eliminar el
    plato — hay que limpiarlo aparte para no acumular basura en el catálogo."""
    tipos = TipoPlatoPage(page)
    tipos.ir_a_tipos_plato()
    if tipos.tipo_plato(tipo).count():
        tipos.eliminar_tipo_plato(tipo)


@pytest.fixture
def plato_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = PlatoPage(page)
    modulo.ir_a_platos()
    return modulo


def test_crear_plato_con_imagen(plato_page: PlatoPage):
    timestamp = int(time.time())
    nombre = f"PLATO QA {timestamp}"
    tipo = f"TIPO QA PLATO {timestamp}"

    plato_page.crear_plato(nombre, tipo)
    expect(plato_page.plato(nombre)).to_be_visible()

    plato_page.eliminar_plato(nombre)
    expect(plato_page.plato(nombre)).to_be_hidden()

    _borrar_tipo_plato_creado(plato_page.page, tipo)


def test_cancelar_creacion_vuelve_al_listado(plato_page: PlatoPage):
    plato_page.ir_a_crear()
    plato_page.volver()
    expect(plato_page.boton_nuevo()).to_be_visible()


def test_editar_plato(plato_page: PlatoPage):
    """Este flujo estuvo roto en la app (ver docs/isuues/menu-platos-editar-no-funciona.md:
    el formulario mandaba `_method=PUT` pero la ruta solo aceptaba POST) y
    ya se corrigió — el test pasa desde el 2026-09-03. Se deja el
    try/finally igual, como red de seguridad para no dejar basura si el
    flujo vuelve a romperse."""
    timestamp = int(time.time())
    nombre_inicial = f"PLATO TEMP {timestamp}"
    nombre_editado = f"PLATO EDIT {timestamp}"
    tipo = f"TIPO QA EDIT {timestamp}"

    plato_page.crear_plato(nombre_inicial, tipo)
    try:
        plato_page.editar_plato(nombre_inicial, nombre_editado)

        expect(plato_page.plato(nombre_editado)).to_be_visible()
        expect(plato_page.plato(nombre_inicial)).to_be_hidden()

        plato_page.eliminar_plato(nombre_editado)
        expect(plato_page.plato(nombre_editado)).to_be_hidden()
    finally:
        plato_page.ir_a_platos()
        if plato_page.plato(nombre_inicial).count():
            plato_page.eliminar_plato(nombre_inicial)
        if plato_page.plato(nombre_editado).count():
            plato_page.eliminar_plato(nombre_editado)
        _borrar_tipo_plato_creado(plato_page.page, tipo)


def test_cancelar_eliminacion(plato_page: PlatoPage):
    timestamp = int(time.time())
    nombre = f"PLATO NO_DEL {timestamp}"
    tipo = f"TIPO QA NODEL {timestamp}"
    plato_page.crear_plato(nombre, tipo)

    plato_page.cancelar_eliminacion(nombre)
    expect(plato_page.plato(nombre)).to_be_visible()

    plato_page.page.wait_for_timeout(500)

    plato_page.eliminar_plato(nombre)
    expect(plato_page.plato(nombre)).to_be_hidden()

    _borrar_tipo_plato_creado(plato_page.page, tipo)
