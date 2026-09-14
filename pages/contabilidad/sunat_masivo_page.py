import re


class SunatMasivoPage:
    def __init__(self, page):
        self.page = page

    def ir_a_sunat_masivo(self):
        self.page.get_by_role("button", name=re.compile("Contabilidad")).click()
        self.page.get_by_role("link", name="Consulta SUNAT Masiva", exact=True).click()

    def consultar(self, tipo_comprobante, serie, numero_desde, numero_hasta=""):
        self.page.locator("#sunat-masivo-tipo").select_option(tipo_comprobante)
        self.page.locator("#sunat-masivo-serie").fill(serie)
        self.page.locator("#sunat-masivo-desde").fill(numero_desde)
        if numero_hasta:
            self.page.locator("#sunat-masivo-hasta").fill(numero_hasta)
        self.page.get_by_role("button", name=re.compile("Consultar SUNAT")).click()

    def filas_resultado(self):
        return self.page.locator("table.table-striped tbody tr")

    def toastr_error(self):
        return self.page.locator("#toast-container .toast-error")
