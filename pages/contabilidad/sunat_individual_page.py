import re


class SunatIndividualPage:
    def __init__(self, page):
        self.page = page

    def ir_a_sunat_individual(self):
        self.page.get_by_role("button", name=re.compile("Contabilidad")).click()
        self.page.get_by_role(
            "link", name="Consulta SUNAT Individual", exact=True
        ).click()

    def consultar(self, tipo_comprobante, serie, numero, fecha_emision, monto):
        self.page.locator("#sunat-individual-tipo").select_option(tipo_comprobante)
        self.page.locator("#sunat-individual-serie").fill(serie)
        self.page.locator("#sunat-individual-numero").fill(numero)
        self.page.locator("#sunat-individual-fecha").fill(fecha_emision)
        self.page.locator("#sunat-individual-monto").fill(monto)
        self.page.get_by_role("button", name=re.compile("Consultar SUNAT")).click()

    def resultado(self):
        return self.page.get_by_text("Resultado", exact=False)

    def badge_estado(self):
        return self.page.locator(".badge.fs-6")

    def toastr_error(self):
        return self.page.locator("#toast-container .toast-error")
