import re

import pytest
from playwright.sync_api import Page, expect

from pages.contabilidad.reporte_contable_page import ReporteContablePage
from pages.login_page import LoginPage


@pytest.fixture
def reporte_contable_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ReporteContablePage(page)
    modulo.ir_a_reporte_contable()
    return modulo


def test_filtrar_por_fechas_y_abrir_pdf(reporte_contable_page: ReporteContablePage):
    reporte_contable_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    pdf = reporte_contable_page.abrir_pdf()
    assert not pdf.is_closed()


def test_exportar_excel(reporte_contable_page: ReporteContablePage):
    reporte_contable_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    descarga = reporte_contable_page.exportar_excel()
    assert descarga.suggested_filename
