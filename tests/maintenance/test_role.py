import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.role_page import RolePage


@pytest.fixture
def role_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = RolePage(page)
    modulo.ir_a_roles()
    return modulo


def test_crear_y_eliminar_rol(role_page: RolePage):
    nombre = f"ROL QA {int(time.time())}"

    role_page.crear(nombre)
    expect(role_page.rol(nombre)).to_be_visible()

    role_page.eliminar(nombre)
    expect(role_page.rol(nombre)).to_be_hidden()


def test_cancelar_creacion_rol(role_page: RolePage):
    role_page.cancelar_creacion()
    expect(role_page.boton_nuevo()).to_be_visible()
