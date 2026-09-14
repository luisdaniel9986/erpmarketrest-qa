import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.colaborador_page import ColaboradorPage
from pages.maintenance.usuario_page import UsuarioPage


@pytest.fixture
def usuario_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = UsuarioPage(page)
    modulo.ir_a_usuarios()
    return modulo


def _dni_unico():
    return f"{int(time.time()) % 100000000:08d}"


def test_crear_y_eliminar_usuario(page: Page, credenciales):
    """El combo de 'Colaborador' del alta de Usuario solo lista colaboradores
    que todavía no tienen un usuario asociado — el ambiente puede no tener
    ninguno disponible, así que este test crea el suyo propio y lo borra al
    final junto con el usuario. No reusa la fixture usuario_page porque acá
    la primera pantalla que hace falta es Colaboradores, no Usuarios."""
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    correo = f"qa.usuario.{int(time.time())}@marketcode.test"
    nombre_colaborador = f"COLABORADOR PARA USUARIO {int(time.time())}"

    colaboradores = ColaboradorPage(page)
    colaboradores.ir_a_colaboradores()
    colaboradores.crear(nombre_colaborador, _dni_unico(), "999888777")

    usuario_page = UsuarioPage(page)
    usuario_page.ir_a_usuarios()
    usuario_page.crear(correo, nombre_colaborador)
    expect(usuario_page.usuario(correo)).to_be_visible()

    usuario_page.eliminar(correo)
    expect(usuario_page.usuario(correo)).to_be_hidden()

    colaboradores.ir_a_colaboradores()
    colaboradores.eliminar(nombre_colaborador)


def test_cancelar_creacion_usuario(usuario_page: UsuarioPage):
    usuario_page.cancelar_creacion()
    expect(usuario_page.boton_nuevo()).to_be_visible()
