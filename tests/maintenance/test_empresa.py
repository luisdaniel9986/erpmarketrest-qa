import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.empresa_page import EmpresaPage


@pytest.fixture
def empresa_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = EmpresaPage(page)
    modulo.ir_a_empresas()
    modulo.editar_primera_empresa()
    return modulo


def test_editar_telefono_empresa_y_revertir(empresa_page: EmpresaPage):
    telefono_original = empresa_page.campo_telefono().input_value()
    telefono_nuevo = "987654321"

    empresa_page.actualizar_telefono(telefono_nuevo)
    empresa_page.page.reload()
    expect(empresa_page.campo_telefono()).to_have_value(telefono_nuevo)

    empresa_page.actualizar_telefono(telefono_original)
    empresa_page.page.reload()
    expect(empresa_page.campo_telefono()).to_have_value(telefono_original)


def test_formulario_de_empresa_carga_datos(empresa_page: EmpresaPage):
    expect(empresa_page.titulo()).to_be_visible()
    expect(empresa_page.campo_telefono()).to_be_visible()
