import re


class CajaPage:
    def __init__(self, page):
        self.page = page

    def ir_a_cajas(self):
        self.page.get_by_role("button", name=re.compile("Cajas")).click()
        self.page.get_by_role("link", name="Caja", exact=True).click()

    def crear_caja(self, nombre):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_placeholder("Nombre de la caja").fill(nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()

    def cancelar_creacion(self):
        self.page.get_by_role("button", name=re.compile("NUEVO")).click()
        self.page.get_by_role("button", name=re.compile("Cancelar")).click()

    def buscar_caja(self, texto):
        self.page.locator(".dt-search input").fill(texto)

    def editar_caja(self, nombre_actual, nuevo_nombre):
        fila = self._fila_de_caja(nombre_actual)
        fila.locator("button").click()
        fila.get_by_text("Editar").click()
        self.page.get_by_placeholder("Nombre de la caja").fill(nuevo_nombre)
        self.page.get_by_role("button", name=re.compile("Guardar")).click()
        self.page.get_by_role("button", name="Sí").click()

    def cancelar_eliminacion(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="No").click()

    def eliminar_caja(self, nombre):
        fila = self._abrir_opciones(nombre)
        fila.get_by_text("Eliminar").click()
        self.page.get_by_role("button", name="Sí").click()

    def caja(self, nombre):
        return self.page.get_by_text(nombre, exact=True)

    def boton_nuevo(self):
        return self.page.get_by_role("button", name=re.compile("NUEVO"))

    def alerta_de_confirmacion(self):
        return self.page.locator(".swal2-container")

    def _fila_de_caja(self, nombre):
        return self.page.locator("tr").filter(has_text=nombre)

    def _abrir_opciones(self, nombre):
        fila = self._fila_de_caja(nombre)
        boton_opciones = fila.locator("button")
            
        # Espera a que el botón esté visible y haz clic
        boton_opciones.wait_for(state="visible")
        boton_opciones.click()
        return fila