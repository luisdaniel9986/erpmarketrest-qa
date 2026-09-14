import re


class ConfiguracionPage:
    """No interactua nunca con la 'Zona de Peligro' (purge) ni con Modo del
    Negocio / Ambiente de facturacion SUNAT — son campos con impacto real
    sobre el tenant y quedan fuera del alcance de este objeto a proposito."""

    def __init__(self, page):
        self.page = page

    def ir_a_configuracion(self):
        self.page.goto("/mantenimiento/configuracion/index")

    def campo_umbral_venta(self):
        return self.page.locator("#config-sales-threshold")

    def guardar(self):
        self.page.get_by_role("button", name=re.compile("Guardar Cambios")).click()
        self.page.get_by_role("button", name=re.compile("Sí, guardar")).click()

    def titulo(self):
        return self.page.get_by_role("heading", name=re.compile("Configuración"))
