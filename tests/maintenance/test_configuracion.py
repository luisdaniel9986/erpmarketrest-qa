import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.configuracion_page import ConfiguracionPage


@pytest.fixture
def configuracion_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ConfiguracionPage(page)
    modulo.ir_a_configuracion()
    return modulo


def test_formulario_de_configuracion_carga(configuracion_page: ConfiguracionPage):
    expect(configuracion_page.titulo()).to_be_visible()
    expect(configuracion_page.campo_umbral_venta()).to_be_visible()


def test_editar_umbral_de_venta_y_revertir(configuracion_page: ConfiguracionPage):
    original = configuracion_page.campo_umbral_venta().input_value()

    configuracion_page.campo_umbral_venta().fill("700")
    configuracion_page.guardar()
    configuracion_page.page.reload()
    expect(configuracion_page.campo_umbral_venta()).to_have_value("700")

    configuracion_page.campo_umbral_venta().fill(original)
    configuracion_page.guardar()
    configuracion_page.page.reload()
    expect(configuracion_page.campo_umbral_venta()).to_have_value(original)
