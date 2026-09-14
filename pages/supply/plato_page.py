import base64
import re
import tempfile
from pathlib import Path

# PNG 1x1 válido, generado en runtime para no versionar un binario en el repo.
_PLACEHOLDER_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def _imagen_de_prueba() -> str:
    ruta = Path(tempfile.gettempdir()) / "qa_plato_placeholder.png"
    if not ruta.exists():
        ruta.write_bytes(base64.b64decode(_PLACEHOLDER_PNG_B64))
    return str(ruta)


class PlatoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_platos(self):
        self.page.goto("/menu/platos")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("NUEVO")).click()

    def crear_plato(self, nombre, tipo_plato_nuevo, precio_venta="10", costo="5", con_imagen=True):
        self.ir_a_crear()
        self.page.locator("#dish-form-name").fill(nombre)
        self.page.get_by_label(re.compile("Precio venta")).fill(precio_venta)
        self.page.get_by_label(re.compile("Costo")).fill(costo)
        self._crear_tipo_plato_rapido(tipo_plato_nuevo)
        if con_imagen:
            # FilePond reemplaza el <input id="dish-form-image"> original por su
            # propio widget; el input real para set_input_files queda anidado
            # como <input type="file"> dentro de .filepond--root.
            self.page.locator(".filepond--root input[type='file']").set_input_files(
                _imagen_de_prueba()
            )
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()
        self.page.wait_for_url(re.compile(r"/menu/platos$"))

    def volver(self):
        self.page.get_by_role("link", name=re.compile("Volver")).click()

    def editar_plato(self, nombre_actual, nuevo_nombre):
        fila = self._abrir_opciones(nombre_actual)
        fila.get_by_text("Editar").click()
        self.page.locator("#dish-form-name").fill(nuevo_nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()
        self.page.wait_for_url(re.compile(r"/menu/platos$"))

    def eliminar_plato(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Sí, eliminar")).click()

    def cancelar_eliminacion(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def plato(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("link", name=re.compile("NUEVO"))

    def _crear_tipo_plato_rapido(self, nombre):
        self.page.get_by_role("button", name=re.compile("Nuevo")).click()
        modal = self.page.locator("#mdl-create-type-dish")
        modal.locator("#create-type-dish-name").fill(nombre)
        modal.get_by_role("button", name=re.compile("Registrar")).click()
        self.page.get_by_role("button", name="Sí").click()

    def _fila(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila(nombre)
        boton_opciones = fila.get_by_test_id(re.compile("row-actions-"))
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila
