import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_exitoso(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])

    expect(page).to_have_url(re.compile(r"/dashboard"))


def test_login_credenciales_invalidas(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], "password-incorrecta")

    expect(login_page.mensaje_error()).to_be_visible()
    expect(page).to_have_url(re.compile(r"/login"))
