import re
import pytest
from playwright.sync_api import Page, expect

from pages.supply.programacion_page import ProgramacionPage
from pages.login_page import LoginPage

# Nota: el módulo solo permite UNA programación ACTIVA a la vez, compartida
# por todas las cajas del tenant. Por eso estos tests solo cubren navegación
# y cancelación — crear, "Cerrar" o "Generar Automático" de verdad pisaría
# el menú vigente de cualquiera usando este mismo ambiente de QA.


@pytest.fixture
def programacion_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ProgramacionPage(page)
    modulo.ir_a_programacion()
    return modulo


def test_listado_visible(programacion_page: ProgramacionPage):
    expect(programacion_page.boton_nueva_programacion()).to_be_visible()
    expect(programacion_page.boton_generar_automatico()).to_be_visible()


def test_ir_a_crear_y_volver(programacion_page: ProgramacionPage):
    programacion_page.ir_a_crear()
    expect(programacion_page.page).to_have_url(re.compile(r"/menu/programacion/create"))

    programacion_page.volver()
    expect(programacion_page.page).to_have_url(re.compile(r"/menu/programacion$"))
