import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.sale.resumenes_page import ResumenesPage


@pytest.fixture
def resumenes_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    modulo = ResumenesPage(page)
    modulo.ir_a_resumenes()
    return modulo


def test_listado_de_resumenes_visible(resumenes_page: ResumenesPage):
    expect(resumenes_page.tabla()).to_be_visible()


def test_filtrar_por_fechas(resumenes_page: ResumenesPage):
    resumenes_page.filtrar_por_fechas("2026-01-01", "2026-12-31")
    expect(resumenes_page.tabla()).to_be_visible()


def test_abrir_y_cerrar_modal_nuevo_resumen(resumenes_page: ResumenesPage):
    resumenes_page.abrir_modal_nuevo()
    expect(resumenes_page.modal_nuevo_resumen()).to_be_visible()

    resumenes_page.cerrar_modal_nuevo()
    expect(resumenes_page.modal_nuevo_resumen()).to_be_hidden()
