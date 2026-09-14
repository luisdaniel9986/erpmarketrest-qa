import re

import pytest
from playwright.sync_api import Page, expect

from pages.sale.notas_devolucion_page import NotasDevolucionPage
from pages.login_page import LoginPage


@pytest.fixture
def notas_devolucion_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = NotasDevolucionPage(page)
    modulo.ir_a_notas_devolucion()
    return modulo


def test_listado_y_filtro_por_fechas(notas_devolucion_page: NotasDevolucionPage):
    # Smoke test de solo lectura: crear una nota de devolución real requiere
    # una venta tipo Ticket/Nota de Venta existente (botón "Nota Devolución"
    # en el listado de Comprobante de Venta) — no se fuerza esa dependencia
    # acá para no anular/afectar ventas reales del ambiente compartido.
    notas_devolucion_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    expect(notas_devolucion_page.tabla()).to_be_visible()
