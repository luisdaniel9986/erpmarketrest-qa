import re

import pytest
from playwright.sync_api import Page, expect

from pages.reports.ventas_page import VentasReportePage
from pages.login_page import LoginPage


@pytest.fixture
def ventas_reporte_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = VentasReportePage(page)
    modulo.ir_a_reporte_ventas()
    return modulo


def test_filtrar_por_fechas_y_abrir_pdf(ventas_reporte_page: VentasReportePage):
    ventas_reporte_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    pdf = ventas_reporte_page.abrir_pdf()
    assert not pdf.is_closed()


def test_exportar_excel(ventas_reporte_page: VentasReportePage):
    ventas_reporte_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    descarga = ventas_reporte_page.exportar_excel()
    assert descarga.suggested_filename
