import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory.nota_ingreso_page import NotaIngresoPage


@pytest.fixture
def nota_ingreso_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = NotaIngresoPage(page)
    modulo.ir_a_notas_ingreso()
    return modulo


def test_abrir_selector_importacion(nota_ingreso_page):
    boton = nota_ingreso_page.abrir_selector_importacion()
    expect(boton).to_be_visible()


def test_volver_desde_nueva_nota(nota_ingreso_page):
    nota_ingreso_page.volver_desde_nueva()
    expect(nota_ingreso_page.page).to_have_url(re.compile(r"/nota-ingreso/index"))


def test_filtrar_y_limpiar_notas(nota_ingreso_page):
    nota_ingreso_page.filtrar(
        "2026-01-01", "2026-12-31", tipo="Ingreso Stock", estado="ACTIVO"
    )
    nota_ingreso_page.limpiar()


def test_buscar_en_tabla(nota_ingreso_page):
    buscador = nota_ingreso_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    buscador.clear()


def test_ver_y_cerrar_detalle(nota_ingreso_page):
    nota_ingreso_page.abrir_primer_detalle()
    expect(nota_ingreso_page.modal_activo()).to_be_visible()
    nota_ingreso_page.cerrar_modal()
    expect(nota_ingreso_page.modal_activo()).to_be_hidden()


def test_cerrar_detalle_con_x(nota_ingreso_page):
    nota_ingreso_page.abrir_primer_detalle()
    expect(nota_ingreso_page.modal_activo()).to_be_visible()
    nota_ingreso_page.cerrar_modal_con_x()
    expect(nota_ingreso_page.modal_activo()).to_be_hidden()


def test_buscar_y_agregar_producto(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.agregar_primer_producto()
    expect(nota_ingreso_page.page.locator("#note-income-quantity")).to_have_value("")


def test_editar_y_eliminar_producto_agregado(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.agregar_primer_producto()
    nota_ingreso_page.editar_producto_agregado("2")
    expect(
        nota_ingreso_page.page.locator("button[data-testid^='btn-delete-row-']")
    ).to_be_visible()
    nota_ingreso_page.eliminar_producto_agregado()
    expect(
        nota_ingreso_page.page.locator("button[data-testid^='btn-delete-row-']")
    ).to_be_hidden()


def test_seleccionar_almacen_y_tipo(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.seleccionar_almacen_y_tipo("MERMAS", "Donación")
    expect(nota_ingreso_page.page.get_by_test_id("note-income-warehouse")).to_contain_text(
        "MERMAS"
    )
    expect(nota_ingreso_page.page.get_by_test_id("note-income-type")).to_contain_text(
        "Donación"
    )


def test_filtros_y_busqueda_selector_productos(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.abrir_selector_productos()
    nota_ingreso_page.filtrar_selector_productos("LLANTAS", "LENOVO")
    buscador = nota_ingreso_page.buscar_en_selector_productos("LENOVO")
    expect(buscador).to_have_value("LENOVO")
    buscador.clear()
    nota_ingreso_page.cerrar_selector_productos()


def test_cerrar_selector_productos_con_x(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.abrir_selector_productos()
    nota_ingreso_page.cerrar_selector_productos_con_x()
    expect(nota_ingreso_page.page.locator("tr[data-testid^='product-row-']:visible")).to_have_count(0)


def test_paginacion_selector_productos(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.abrir_selector_productos()
    siguiente = nota_ingreso_page.boton_paginacion_selector("Next")
    expect(siguiente).to_be_enabled()
    nota_ingreso_page.ir_a_pagina_selector("Next")
    expect(nota_ingreso_page.boton_paginacion_selector("Previous")).to_be_enabled()
    nota_ingreso_page.ir_a_pagina_selector("Previous")
    nota_ingreso_page.ir_a_pagina_selector("Last")
    expect(nota_ingreso_page.boton_paginacion_selector("First")).to_be_enabled()
    nota_ingreso_page.ir_a_pagina_selector("First")


def test_registrar_nota_ingreso(nota_ingreso_page):
    nota_ingreso_page.abrir_nueva()
    nota_ingreso_page.agregar_primer_producto()
    nota_ingreso_page.registrar_nota()
    expect(nota_ingreso_page.page).to_have_url(re.compile(r"/nota-ingreso/index"))


def test_paginacion_notas(nota_ingreso_page):
    primero = nota_ingreso_page.boton_paginacion("First")
    anterior = nota_ingreso_page.boton_paginacion("Previous")
    siguiente = nota_ingreso_page.boton_paginacion("Next")
    ultimo = nota_ingreso_page.boton_paginacion("Last")

    for boton in (primero, anterior, siguiente, ultimo):
        expect(boton).to_be_visible()

    expect(primero).to_be_disabled()
    expect(anterior).to_be_disabled()
    if siguiente.is_enabled():
        nota_ingreso_page.ir_a_pagina("Next")
        expect(anterior).to_be_enabled()
        nota_ingreso_page.ir_a_pagina("Previous")
        nota_ingreso_page.ir_a_pagina("Last")
        expect(primero).to_be_enabled()
        nota_ingreso_page.ir_a_pagina("First")
    else:
        expect(ultimo).to_be_disabled()
