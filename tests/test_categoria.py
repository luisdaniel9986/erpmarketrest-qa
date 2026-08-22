import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from pages.categoria_page import CategoriaPage
from pages.login_page import LoginPage


@pytest.fixture
def categoria_page(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    categoria_page = CategoriaPage(page)
    categoria_page.ir_a_categorias()
    return categoria_page


def test_importar_categorias(categoria_page: CategoriaPage):
    ruta_importacion = (
        Path(__file__).parents[1]
        / "datos"
        / "formato_import_categorias.xlsx"
    )

    categoria_page.importar_categorias(ruta_importacion)
    expect(categoria_page.boton_importar()).to_be_visible()


def test_cancelar_importacion(categoria_page: CategoriaPage):
    categoria_page.cancelar_importacion()
    expect(categoria_page.boton_importar()).to_be_visible()


def test_crear_categoria(categoria_page: CategoriaPage):
    nombre = "CATEGORIA10002"

    categoria_page.crear_categoria(nombre)

    expect(categoria_page.categoria(nombre)).to_be_visible()


def test_cancelar_creacion(categoria_page: CategoriaPage):
    categoria_page.cancelar_creacion()
    expect(categoria_page.boton_nuevo()).to_be_visible()


def test_filtrar_categorias_activas(categoria_page: CategoriaPage):
    categoria_page.filtrar_por_estado("ACTIVO")
    categoria_page.limpiar_filtro()


def test_editar_categoria(categoria_page: CategoriaPage):
    categoria_page.editar_categoria("CATEGORIA10016")
    expect(categoria_page.categoria("CATEGORIA10016")).to_be_visible()


def test_cancelar_eliminacion(categoria_page: CategoriaPage):
    categoria_page.cancelar_eliminacion("CATEGORIA10017")
    expect(categoria_page.categoria("CATEGORIA10017")).to_be_visible()


def test_eliminar_y_reactivar_categoria(categoria_page: CategoriaPage):
    categoria_page.eliminar_categoria("CATEGORIA10017")
    expect(categoria_page.alerta_de_confirmacion()).to_be_hidden()

    categoria_page.filtrar_por_estado("ANULADO")
    categoria_page.reactivar_categoria("CATEGORIA10017")
    categoria_page.limpiar_filtro()
    expect(categoria_page.categoria("CATEGORIA10017")).to_be_visible()
