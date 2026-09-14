import re

import pytest
from playwright.sync_api import Page, expect

from pages.sale.notas_credito_page import NotasCreditoPage
from pages.login_page import LoginPage


@pytest.fixture
def notas_credito_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = NotasCreditoPage(page)
    modulo.ir_a_notas_credito()
    return modulo


def test_listado_y_filtro_por_fechas(notas_credito_page: NotasCreditoPage):
    # Smoke test de solo lectura: crear una nota de crédito real requiere una
    # venta ya aceptada por SUNAT (botón "Nota Crédito" en el listado de
    # Comprobante de Venta) — no se fuerza esa dependencia acá para no generar
    # documentos SUNAT reales desde la suite automatizada.
    notas_credito_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    expect(notas_credito_page.tabla()).to_be_visible()
