import re

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.nota_salida_page import NotaSalidaPage


@pytest.fixture
def nota_salida_page(page: Page, credenciales):
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = NotaSalidaPage(page)
    modulo.ir_a_notas_salida()
    return modulo


def test_volver_desde_nueva_nota(nota_salida_page):
    nota_salida_page.volver_desde_nueva()
    expect(nota_salida_page.page).to_have_url(re.compile(r"/nota-salida/index"))


def test_filtrar_y_limpiar_notas(nota_salida_page):
    nota_salida_page.filtrar(
        "2026-01-01", "2026-12-31", tipo="Salida Stock", estado="ACTIVO"
    )
    nota_salida_page.limpiar()


def test_buscar_en_tabla(nota_salida_page):
    buscador = nota_salida_page.buscar_en_tabla("BUSQUEDA_QA_SIN_RESULTADOS")
    expect(buscador).to_have_value("BUSQUEDA_QA_SIN_RESULTADOS")
    buscador.clear()


def test_ver_y_cerrar_detalle(nota_salida_page):
    nota_salida_page.abrir_primer_detalle()
    expect(nota_salida_page.modal_activo()).to_be_visible()
    nota_salida_page.cerrar_modal()
    expect(nota_salida_page.modal_activo()).to_be_hidden()


def test_cerrar_detalle_con_x(nota_salida_page):
    nota_salida_page.abrir_primer_detalle()
    nota_salida_page.cerrar_modal_con_x()
    expect(nota_salida_page.modal_activo()).to_be_hidden()


def test_buscar_y_agregar_producto(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.agregar_primer_producto()
    expect(nota_salida_page.page.locator("#note-release-quantity")).to_have_value("")


def test_editar_y_eliminar_producto_agregado(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.agregar_primer_producto()
    nota_salida_page.editar_producto_agregado("2")
    expect(
        nota_salida_page.page.locator("button[data-testid^='btn-delete-row-']")
    ).to_be_visible()
    nota_salida_page.eliminar_producto_agregado()
    expect(
        nota_salida_page.page.locator("button[data-testid^='btn-delete-row-']")
    ).to_be_hidden()


def test_cerrar_edicion_producto(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.agregar_primer_producto()
    nota_salida_page.abrir_edicion_producto_agregado()
    nota_salida_page.cerrar_edicion_producto()
    expect(nota_salida_page.modal_activo()).to_be_hidden()


def test_cerrar_edicion_producto_con_x(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.agregar_primer_producto()
    nota_salida_page.abrir_edicion_producto_agregado()
    nota_salida_page.cerrar_edicion_producto_con_x()
    expect(nota_salida_page.modal_activo()).to_be_hidden()


def test_seleccionar_almacenes_y_tipo(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.seleccionar_almacenes_y_tipo(
        "CENTRAL", "MERMAS", "Salida Stock"
    )
    expect(nota_salida_page.page.locator("#note-release-warehouse-origin")).to_have_value(
        re.compile(r".+")
    )
    expect(nota_salida_page.page.locator("#note-release-warehouse-destiny")).to_have_value(
        re.compile(r".+")
    )


def test_limpiar_almacenes_y_tipo_con_x(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.seleccionar_almacenes_y_tipo(
        "CENTRAL", "MERMAS", "Salida Stock"
    )
    for selector_id in (
        "note-release-warehouse-origin",
        "note-release-warehouse-destiny",
        "note-release-type",
    ):
        nota_salida_page.limpiar_selector_con_x(selector_id)
        expect(nota_salida_page.page.locator(f"#{selector_id}")).to_have_value("")


def test_filtros_y_busqueda_selector_productos(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.abrir_selector_productos()
    nota_salida_page.filtrar_selector_productos("LLANTAS", "LENOVO")
    buscador = nota_salida_page.buscar_en_selector_productos("LENOVO")
    expect(buscador).to_have_value("LENOVO")
    buscador.clear()
    nota_salida_page.cerrar_selector_productos()


def test_cerrar_selector_productos_con_x(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.abrir_selector_productos()
    nota_salida_page.cerrar_selector_productos_con_x()
    expect(nota_salida_page.page.locator("tr[data-testid^='product-row-']:visible")).to_have_count(0)


def test_paginacion_selector_productos(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.abrir_selector_productos()
    expect(nota_salida_page.boton_paginacion("Next")).to_be_enabled()
    nota_salida_page.ir_a_pagina("Next")
    expect(nota_salida_page.boton_paginacion("Previous")).to_be_enabled()
    nota_salida_page.ir_a_pagina("Previous")
    nota_salida_page.ir_a_pagina("Last")
    expect(nota_salida_page.boton_paginacion("First")).to_be_enabled()
    nota_salida_page.ir_a_pagina("First")


def test_registrar_nota_salida(nota_salida_page):
    nota_salida_page.abrir_nueva()
    nota_salida_page.seleccionar_almacenes_y_tipo(
        "CENTRAL", "MERMAS", "Salida Stock"
    )
    nota_salida_page.agregar_primer_producto()
    nota_salida_page.registrar_nota()
    expect(nota_salida_page.page).to_have_url(re.compile(r"/nota-salida/index"))


def test_paginacion_notas(nota_salida_page):
    primero = nota_salida_page.boton_paginacion("First")
    anterior = nota_salida_page.boton_paginacion("Previous")
    siguiente = nota_salida_page.boton_paginacion("Next")
    ultimo = nota_salida_page.boton_paginacion("Last")
    for boton in (primero, anterior, siguiente, ultimo):
        expect(boton).to_be_visible()
    expect(primero).to_be_disabled()
    expect(anterior).to_be_disabled()
    if siguiente.is_enabled():
        nota_salida_page.ir_a_pagina("Next")
        expect(anterior).to_be_enabled()
        nota_salida_page.ir_a_pagina("Previous")
        nota_salida_page.ir_a_pagina("Last")
        expect(primero).to_be_enabled()
        nota_salida_page.ir_a_pagina("First")
    else:
        expect(ultimo).to_be_disabled()
