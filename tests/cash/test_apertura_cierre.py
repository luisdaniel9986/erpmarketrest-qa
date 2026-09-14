import re

import pytest
from playwright.sync_api import Page, expect

from pages.cash.apertura_cierre_page import AperturaCierrePage
from pages.login_page import LoginPage


@pytest.fixture
def apertura_cierre_page(page: Page, credenciales):
    """Solo lectura con el usuario admin — ver test_abrir_y_cerrar_caja para
    el flujo real, que requiere el usuario CAJERO (ver credenciales_cajero)."""
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = AperturaCierrePage(page)
    modulo.ir_a_apertura_cierre()
    return modulo


def test_lista_de_aperturas_visible(apertura_cierre_page: AperturaCierrePage):
    expect(apertura_cierre_page.titulo()).to_be_visible()
    expect(apertura_cierre_page.boton_nuevo()).to_be_visible()


def test_abrir_y_cerrar_caja(page: Page, credenciales_cajero):
    """Solo el rol CAJERO puede aperturar caja (regla de negocio real de
    este ambiente: 'SOLO CAJEROS PUEDEN ABRIR UNA CAJA'), y además exige al
    menos un mesero/vendedor disponible para la sede ('DEBE SELECCIONAR AL
    MENOS UN MESERO O VENDEDOR PARA LA CAJA'). Si el ambiente todavía no
    tiene ese personal cargado para la sede del cajero de prueba, el test se
    salta en vez de fallar — es un dato de precondición que le corresponde
    al equipo de datos de prueba, no un bug de este test."""
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales_cajero["email"], credenciales_cajero["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = AperturaCierrePage(page)
    modulo.ir_a_apertura_cierre()

    modulo.boton_nuevo().click()
    modal = page.locator("#mdl-open-cash")
    combo = modal.get_by_test_id("open-cash-select")
    combo.click()
    combo.locator(".ts-dropdown .option").first.click()
    modal.locator("#open-cash-shift").select_option(index=1)
    modal.locator("#open-cash-initial-amount").fill("100")

    if modal.locator('[data-testid^="server-check-"]').count() == 0:
        pytest.skip(
            "No hay mesero/vendedor disponible para la sede del cajero de "
            "prueba en este ambiente — precondición de datos, no de código."
        )

    modal.locator('[data-testid^="server-check-"]').first.check()
    modal.get_by_role("button", name=re.compile("Guardar")).click()
    page.get_by_role("button", name="Sí").click()
    modal.wait_for(state="hidden", timeout=10_000)

    expect(modulo.fila_abierta()).to_be_visible()

    modulo.cerrar_ultima_caja_abierta("100")
    expect(page.locator("tr").filter(has_text="ABIERTO")).to_have_count(0)
