import re


class ProgramacionPage:
    """Solo cubre navegación y cancelación: el sistema solo permite UNA
    programación ACTIVA a la vez (compartida por todas las cajas del tenant),
    así que crear/cerrar/generar automático desde un test automatizado
    pisaría el menú vigente de cualquiera que esté usando este ambiente de
    QA en simultáneo. Ver docs/isuues si se agrega cobertura de creación
    más adelante, coordinando con el equipo un tenant dedicado."""

    def __init__(self, page):
        self.page = page

    def ir_a_programacion(self):
        self.page.goto("/menu/programacion")

    def ir_a_crear(self):
        self.page.get_by_role("link", name=re.compile("Nueva Programaci")).click()

    def volver(self):
        self.page.get_by_role("link", name=re.compile("Volver")).first.click()

    def boton_nueva_programacion(self):
        return self.page.get_by_role("link", name=re.compile("Nueva Programaci"))

    def boton_generar_automatico(self):
        return self.page.get_by_role("button", name=re.compile("Generar Autom"))
