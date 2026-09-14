import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.bank_account_page import BankAccountPage


@pytest.fixture
def bank_account_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = BankAccountPage(page)
    modulo.ir_a_cuentas_bancarias()
    return modulo


def test_crear_cuenta(bank_account_page: BankAccountPage):
    timestamp = int(time.time())
    nombre = f"CUENTA QA {timestamp}"

    bank_account_page.crear_cuenta(nombre, titular="QA TESTER", numero_cuenta=f"{timestamp}")
    expect(bank_account_page.cuenta(nombre)).to_be_visible()

    bank_account_page.eliminar_cuenta(nombre)
    expect(bank_account_page.cuenta(nombre)).to_be_hidden()


def test_cancelar_creacion(bank_account_page: BankAccountPage):
    bank_account_page.cancelar_creacion()
    expect(bank_account_page.boton_nuevo()).to_be_visible()


def test_buscar_cuenta(bank_account_page: BankAccountPage):
    timestamp = int(time.time())
    nombre = f"CUENTA BUSCAR {timestamp}"
    bank_account_page.crear_cuenta(nombre, titular="QA TESTER", numero_cuenta=f"{timestamp}")

    bank_account_page.buscar_cuenta(nombre)
    expect(bank_account_page.cuenta(nombre)).to_be_visible()

    bank_account_page.eliminar_cuenta(nombre)


def test_editar_cuenta(bank_account_page: BankAccountPage):
    timestamp = int(time.time())
    nombre_inicial = f"CUENTA TEMP {timestamp}"
    nombre_editado = f"CUENTA EDIT {timestamp}"

    bank_account_page.crear_cuenta(nombre_inicial, titular="QA TESTER", numero_cuenta=f"{timestamp}")
    bank_account_page.editar_cuenta(nombre_inicial, nombre_editado)

    expect(bank_account_page.cuenta(nombre_editado)).to_be_visible()
    expect(bank_account_page.cuenta(nombre_inicial)).to_be_hidden()

    bank_account_page.eliminar_cuenta(nombre_editado)
    expect(bank_account_page.cuenta(nombre_editado)).to_be_hidden()


def test_cancelar_eliminacion(bank_account_page: BankAccountPage):
    timestamp = int(time.time())
    nombre = f"CUENTA NO_DEL {timestamp}"
    bank_account_page.crear_cuenta(nombre, titular="QA TESTER", numero_cuenta=f"{timestamp}")

    bank_account_page.cancelar_eliminacion(nombre)
    expect(bank_account_page.cuenta(nombre)).to_be_visible()

    bank_account_page.page.wait_for_timeout(500)

    bank_account_page.eliminar_cuenta(nombre)
    expect(bank_account_page.cuenta(nombre)).to_be_hidden()


def test_eliminar_cuenta(bank_account_page: BankAccountPage):
    timestamp = int(time.time())
    nombre = f"CUENTA DEL {timestamp}"
    bank_account_page.crear_cuenta(nombre, titular="QA TESTER", numero_cuenta=f"{timestamp}")

    bank_account_page.eliminar_cuenta(nombre)
    expect(bank_account_page.alerta_de_confirmacion()).to_be_hidden()
    expect(bank_account_page.cuenta(nombre)).to_be_hidden()
