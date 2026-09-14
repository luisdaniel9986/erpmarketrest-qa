class DashboardPage:
    def __init__(self, page):
        self.page = page

    def ir_a_dashboard(self):
        # El grupo "Dashboard" del sidebar solo aparece para usuarios ADMIN
        # (ver app/Http/Middleware/HandleInertiaRequests.php), así que se navega
        # directo a la ruta en vez de depender de un click en el sidebar.
        self.page.goto("/dashboard/dashboard/index")

    def titulo_salud_negocio(self):
        return self.page.get_by_text("Salud del negocio")

    def titulo_analisis_mes(self):
        return self.page.get_by_text("Análisis del mes")

    def titulo_analisis_anio(self):
        return self.page.get_by_text("Análisis del año")

    def tabla_stock_minimo(self):
        return self.page.locator("#table_stock_min")

    def exportar_stock_minimo(self):
        with self.page.expect_download() as descarga:
            self.page.get_by_test_id("excel-stock-minimo").click()
        return descarga.value
