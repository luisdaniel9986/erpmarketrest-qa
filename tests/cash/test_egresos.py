import re
import time

import pytest
from playwright.sync_api import Page, expect

from pages.cash.apertura_cierre_page import AperturaCierrePage
from pages.cash.egresos_page import EgresosPage
from pages.login_page import LoginPage
from pages.maintenance.cost_center_page import CostCenterPage


@pytest.fixture
def egresos_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = EgresosPage(page)
    modulo.ir_a_egresos()
    return modulo


def test_crear_y_anular_egreso(page: Page, credenciales_cajero):
    """Registrar un egreso exige estar 'dentro' de una caja abierta (regla
    real: 'NO FORMAS PARTE DE UNA CAJA ABIERTA'), así que este test abre una
    caja como CAJERO primero. Si el ambiente no tiene mesero/vendedor
    cargado para la sede (precondición de datos, ver test_apertura_cierre),
    no hay forma de abrir una caja todavía y el test se salta."""
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales_cajero["email"], credenciales_cajero["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    apertura = AperturaCierrePage(page)
    apertura.ir_a_apertura_cierre()
    apertura.boton_nuevo().click()
    modal = page.locator("#mdl-open-cash")
    combo = modal.get_by_test_id("open-cash-select")
    combo.click()
    combo.locator(".ts-dropdown .option").first.click()
    modal.locator("#open-cash-shift").select_option(index=1)
    modal.locator("#open-cash-initial-amount").fill("100")
    if modal.locator('[data-testid^="server-check-"]').count() == 0:
        pytest.skip(
            "No hay mesero/vendedor disponible para abrir una caja en este "
            "ambiente — precondición de datos, no de código."
        )
    modal.locator('[data-testid^="server-check-"]').first.check()
    modal.get_by_role("button", name=re.compile("Guardar")).click()
    page.get_by_role("button", name="Sí").click()
    modal.wait_for(state="hidden", timeout=10_000)

    numero = f"EGR-QA-{int(time.time())}"
    centro_costo = f"CC QA {int(time.time())}"

    egresos_page = EgresosPage(page)
    egresos_page.ir_a_egresos()
    egresos_page.ir_a_crear()
    egresos_page.completar_egreso(numero, "GASTO DE PRUEBA QA", "15.50", centro_costo=centro_costo)
    egresos_page.guardar()

    expect(page).to_have_url(re.compile(r"/cajas/egresos/index"))
    fila = egresos_page.fila_por_numero(numero)
    expect(fila).to_be_visible()

    egresos_page.anular(numero)
    expect(fila).to_be_hidden()

    # Limpieza: cerramos la caja que abrimos y borramos el centro de costos
    # si lo tuvimos que crear nosotros (ambiente sin ninguno cargado).
    apertura.ir_a_apertura_cierre()
    apertura.cerrar_ultima_caja_abierta("100")

    centros = CostCenterPage(page)
    centros.ir_a_centros_costo()
    if centros.centro_costo(centro_costo).count():
        centros.eliminar_centro_costo(centro_costo)


def test_buscar_egreso_sin_resultados(egresos_page: EgresosPage):
    buscador = egresos_page.buscar("EGRESO_QA_SIN_RESULTADOS_XYZ")
    expect(buscador).to_have_value("EGRESO_QA_SIN_RESULTADOS_XYZ")
    expect(egresos_page.page.locator("table tbody")).to_contain_text(
        "No hay datos disponibles en la tabla"
    )
