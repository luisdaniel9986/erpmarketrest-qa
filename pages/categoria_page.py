class CategoriaPage:
    def __init__(self, page):
        self.page = page

    def ir_a_categorias(self):
        self.page.goto("/inventario/categorias/index")

    def crear_categoria(self, nombre):
        self.page.get_by_role("button", name=" NUEVO").click()
        self.page.get_by_role("textbox", name="Nombre de la categoría").fill(nombre)
        self.page.get_by_role("button", name=" Guardar").click()
        self.page.get_by_role("button", name="Sí").click()
