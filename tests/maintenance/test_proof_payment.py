import re
import time
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.maintenance.proof_payment_page import ProofPaymentPage


@pytest.fixture
def proof_payment_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ProofPaymentPage(page)
    modulo.ir_a_comprobantes()
    return modulo


def test_crear_comprobante(proof_payment_page: ProofPaymentPage):
    descripcion = f"COMPROBANTE TEST {int(time.time())}"

    proof_payment_page.crear_comprobante(descripcion)
    expect(proof_payment_page.comprobante(descripcion)).to_be_visible()

    proof_payment_page.eliminar_comprobante(descripcion)
    expect(proof_payment_page.comprobante(descripcion)).to_be_hidden()


def test_cancelar_creacion(proof_payment_page: ProofPaymentPage):
    proof_payment_page.cancelar_creacion()
    expect(proof_payment_page.boton_nuevo()).to_be_visible()


def test_buscar_comprobante(proof_payment_page: ProofPaymentPage):
    descripcion = f"COMPROBANTE BUSCAR {int(time.time())}"
    proof_payment_page.crear_comprobante(descripcion)

    proof_payment_page.buscar_comprobante(descripcion)
    expect(proof_payment_page.comprobante(descripcion)).to_be_visible()

    proof_payment_page.eliminar_comprobante(descripcion)


def test_editar_comprobante(proof_payment_page: ProofPaymentPage):
    timestamp = int(time.time())
    descripcion_inicial = f"COMPROBANTE TEMP {timestamp}"
    descripcion_editada = f"COMPROBANTE EDIT {timestamp}"

    proof_payment_page.crear_comprobante(descripcion_inicial)
    proof_payment_page.editar_comprobante(descripcion_inicial, descripcion_editada)

    expect(proof_payment_page.comprobante(descripcion_editada)).to_be_visible()
    expect(proof_payment_page.comprobante(descripcion_inicial)).to_be_hidden()

    proof_payment_page.eliminar_comprobante(descripcion_editada)
    expect(proof_payment_page.comprobante(descripcion_editada)).to_be_hidden()


def test_cancelar_eliminacion(proof_payment_page: ProofPaymentPage):
    descripcion = f"COMPROBANTE NO_DEL {int(time.time())}"
    proof_payment_page.crear_comprobante(descripcion)

    proof_payment_page.cancelar_eliminacion(descripcion)
    expect(proof_payment_page.comprobante(descripcion)).to_be_visible()

    proof_payment_page.page.wait_for_timeout(500)

    proof_payment_page.eliminar_comprobante(descripcion)
    expect(proof_payment_page.comprobante(descripcion)).to_be_hidden()


def test_eliminar_comprobante(proof_payment_page: ProofPaymentPage):
    descripcion = f"COMPROBANTE DEL {int(time.time())}"
    proof_payment_page.crear_comprobante(descripcion)

    proof_payment_page.eliminar_comprobante(descripcion)
    expect(proof_payment_page.alerta_de_confirmacion()).to_be_hidden()
    expect(proof_payment_page.comprobante(descripcion)).to_be_hidden()
