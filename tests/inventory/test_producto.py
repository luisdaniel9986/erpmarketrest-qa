import re
from pathlib import Path
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.inventory.producto_page import ProductoPage


DATOS = Path(__file__).resolve().parents[2] / "datos"
IMAGEN_PRODUCTO = DATOS / "p_korgpa700.jpeg"
ARCHIVO_IMPORTACION = DATOS / "formato_importacion_productos.xlsx"

TIMEOUT_CREACION_MS = 60_000


def _sufijo_unico():
    return uuid4().hex[:8].upper()


def datos_producto_unico():
    """Datos de un producto nuevo; nombre y códigos únicos para no chocar entre corridas."""
    sufijo = _sufijo_unico()
    return {
        "nombre": f"PRODUCTO_QA_{sufijo}",
        "categoria": "TECLADOS",
        "descripcion": "Producto creado por pruebas QA",
        "marca": "NOKIA",
        "precio_venta": "185",
        "precio_compra": "56",
        "unidad": r"AR.*ARROBA",
        "stock_inicial": "55",
        "stock_minimo": "19",
        "codigo_fabrica": f"QA-{sufijo}",
        "codigo_barras": str(uuid4().int)[-12:],
    }


def crear_producto_qa(producto_page):
    """Crea un producto único por la UI y devuelve su nombre."""
    datos = datos_producto_unico()
    producto_page.crear(datos, IMAGEN_PRODUCTO)
    return datos["nombre"]


@pytest.fixture
def producto_page(page: Page, credenciales):
    """ProductoPage lista para usar: sesión iniciada y ubicada en el listado de productos."""
    login = LoginPage(page)
    login.ir_a_login()
    login.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
    modulo = ProductoPage(page)
    modulo.ir_a_productos()
    return modulo


# --- Importar / exportar ---

def test_exportar_productos(producto_page):
    descarga = producto_page.exportar()
    assert descarga.suggested_filename


def test_importar_productos(producto_page):
    producto_page.importar(ARCHIVO_IMPORTACION)
    expect(producto_page.boton_importar()).to_be_visible()


def test_cancelar_importacion(producto_page):
    producto_page.cancelar_importacion()
    expect(producto_page.modal()).to_be_hidden()
    expect(producto_page.boton_importar()).to_be_visible()


def test_cerrar_importacion_con_x(producto_page):
    producto_page.cerrar_importacion()
    expect(producto_page.modal()).to_be_hidden()
    expect(producto_page.boton_importar()).to_be_visible()


# --- Creación ---

def test_crear_producto(producto_page):
    nombre = crear_producto_qa(producto_page)
    expect(producto_page.producto(nombre)).to_be_visible(timeout=TIMEOUT_CREACION_MS)


def test_cancelar_creacion(producto_page):
    producto_page.cancelar_creacion()
    expect(producto_page.boton_nuevo()).to_be_visible()


def test_volver_desde_creacion(producto_page):
    producto_page.volver_desde_creacion()
    expect(producto_page.boton_nuevo()).to_be_visible()


# --- Registro rápido de categoría y marca ---

def test_cancelar_nueva_categoria(producto_page):
    producto_page.cancelar_nueva_categoria()
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.formulario_producto()).to_be_visible()


def test_cerrar_nueva_categoria_con_x(producto_page):
    producto_page.cerrar_nueva_categoria()
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.formulario_producto()).to_be_visible()


def test_registrar_nueva_categoria(producto_page):
    nombre = f"CATEGORIA_PRODUCTO_QA_{_sufijo_unico()}"
    producto_page.registrar_nueva_categoria(nombre)
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.categoria_seleccionada()).to_contain_text(nombre)


def test_cancelar_nueva_marca(producto_page):
    producto_page.cancelar_nueva_marca()
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.formulario_producto()).to_be_visible()


def test_cerrar_nueva_marca_con_x(producto_page):
    producto_page.cerrar_nueva_marca()
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.formulario_producto()).to_be_visible()


def test_registrar_nueva_marca(producto_page):
    nombre = f"MARCA_PRODUCTO_QA_{_sufijo_unico()}"
    producto_page.registrar_nueva_marca(nombre)
    expect(producto_page.modal_activo()).to_be_hidden()
    expect(producto_page.opcion_marca(nombre)).to_be_attached()


# --- Filtros ---

def test_filtrar_productos_activos(producto_page):
    producto_page.filtrar_por_estado("ACTIVO")
    producto_page.limpiar_filtro()
    expect(producto_page.boton_nuevo()).to_be_visible()


# --- Edición ---

def test_editar_producto(producto_page):
    nombre = producto_page.primer_producto_nombre()
    producto_page.editar(nombre)
    expect(producto_page.producto(nombre)).to_be_visible()


def test_cancelar_edicion(producto_page):
    nombre = producto_page.primer_producto_nombre()
    producto_page.cancelar_edicion(nombre)
    expect(producto_page.boton_nuevo()).to_be_visible()


def test_volver_desde_edicion(producto_page):
    nombre = producto_page.primer_producto_nombre()
    producto_page.volver_desde_edicion(nombre)
    expect(producto_page.boton_nuevo()).to_be_visible()


# --- Eliminación y reactivación ---

def test_cancelar_eliminacion(producto_page):
    nombre = producto_page.primer_producto_nombre()
    producto_page.cancelar_eliminacion(nombre)
    expect(producto_page.producto(nombre)).to_be_visible()


def test_eliminar_y_reactivar_producto(producto_page):
    # Crea su propio producto para no eliminar datos que usen otros tests.
    nombre = crear_producto_qa(producto_page)

    producto_page.eliminar(nombre)
    expect(producto_page.alerta_de_confirmacion()).to_be_hidden()

    producto_page.filtrar_por_estado("ANULADO")
    producto_page.aplicar_filtro()
    expect(producto_page.producto(nombre)).to_be_visible()

    producto_page.reactivar(nombre)
    producto_page.limpiar_filtro()
    expect(producto_page.producto(nombre)).to_be_visible()
