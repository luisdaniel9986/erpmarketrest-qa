import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.categoria_page import CategoriaPage


def test_crear_categoria(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    categoria_page = CategoriaPage(page)
    categoria_page.ir_a_categorias()
    categoria_page.crear_categoria("C3")

    expect(page.get_by_text("C3")).to_be_visible()
