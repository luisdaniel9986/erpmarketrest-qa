import re

import pytest
from playwright.sync_api import Page, expect

from pages.dashboard.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.fixture
def dashboard_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = DashboardPage(page)
    modulo.ir_a_dashboard()
    return modulo


def test_dashboard_carga_widgets_principales(dashboard_page: DashboardPage):
    expect(dashboard_page.titulo_salud_negocio()).to_be_visible()
    expect(dashboard_page.titulo_analisis_mes()).to_be_visible()
    expect(dashboard_page.titulo_analisis_anio()).to_be_visible()
    expect(dashboard_page.tabla_stock_minimo()).to_be_visible()


def test_dashboard_exportar_stock_minimo(dashboard_page: DashboardPage):
    descarga = dashboard_page.exportar_stock_minimo()
    assert descarga.suggested_filename
