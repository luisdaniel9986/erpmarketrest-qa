# El patrón de diseño de este proyecto: Page Object Model

Antes de escribir o tocar cualquier test, conviene entender cómo está armado el repo — así cada archivo nuevo que agregues (tuyo o de un compañero) queda en el lugar correcto y con la forma correcta, en vez de mezclado todo en un archivo gigante.

## El problema que resuelve

Sin ningún patrón, la forma más directa de escribir un test es poner los selectores sueltos, directo en el test:

```python
def test_login_exitoso(page, credenciales):
    page.goto("/login")
    page.get_by_label("Correo Electrónico").fill(credenciales["email"])
    page.get_by_label("Contraseña").fill(credenciales["password"])
    page.get_by_role("button", name="Iniciar Sesión").click()
    expect(page).to_have_url(re.compile(r"/dashboard"))
```

Funciona para un test. El problema aparece cuando tenés 10 tests que necesitan loguearse: si el botón "Iniciar Sesión" cambia de texto, o el campo cambia de label, tenés que salir a buscar y arreglar el selector en los 10 archivos, uno por uno. Es exactamente lo que le pasó a `tests/prueba.py` en este repo — código de Codegen pegado tal cual, sin estructura, difícil de mantener apenas crece.

## La solución: separar "cómo interactuar con la pantalla" de "qué se está probando"

**Page Object Model (POM)** es el patrón que usa este proyecto: cada pantalla del sistema tiene una clase, en `pages/`, que agrupa todos sus selectores y acciones. Los tests, en `tests/`, no conocen ningún selector — solo usan los métodos de esa clase.

```
erpmarketrest-qa/
├── pages/                    ← "cómo se interactúa con cada pantalla"
│   ├── login_page.py             clase LoginPage
│   └── categoria_page.py         clase CategoriaPage
├── tests/                    ← "qué se está verificando"
│   ├── test_login.py             usa LoginPage
│   └── test_categoria.py         usa LoginPage + CategoriaPage
├── conftest.py                ← fixtures compartidas (ej. credenciales)
└── pytest.ini                 ← configuración (base_url, etc.)
```

### Ejemplo real: `pages/login_page.py`

```python
class LoginPage:
    def __init__(self, page):
        self.page = page

    def ir_a_login(self):
        self.page.goto("/login")

    def login(self, email, password):
        self.page.get_by_label("Correo Electrónico").fill(email)
        self.page.get_by_label("Contraseña").fill(password)
        self.page.get_by_role("button", name="Iniciar Sesión").click()

    def mensaje_error(self):
        return self.page.locator(".alert-danger")
```

Todo lo que sabe sobre *cómo* se ve y se usa la pantalla de login vive acá adentro: qué labels tienen los campos, qué texto tiene el botón, dónde aparece el mensaje de error.

### El test correspondiente, `tests/test_login.py`

```python
def test_login_exitoso(page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
```

El test no sabe nada de labels ni botones — solo orquesta pasos (`ir_a_login`, `login`) y verifica un resultado (`expect(...)`). Se lee de arriba a abajo como una historia, sin ruido técnico en el medio.

## La ventaja concreta

Si mañana el botón "Iniciar Sesión" cambia de texto, arreglás **una sola línea**, en `LoginPage.login()` — no salís a buscar en cada test que hace login. Todos los tests que usan `LoginPage` se arreglan solos.

Esto ya se aplicó una segunda vez en el repo con Categorías — comparalo, es el mismo patrón calcado:

`pages/categoria_page.py`:
```python
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
```

## La regla para cualquier flujo nuevo

1. **Un archivo por pantalla en `pages/`**, con una clase que agrupa sus selectores y acciones (`ir_a_<pantalla>`, la acción principal, y cualquier verificación auxiliar como `mensaje_error`).
2. **El test en `tests/` solo orquesta y verifica** — nunca tiene un `page.get_by_...` suelto. Si ves un selector directo en un archivo de `tests/`, es señal de que falta moverlo a `pages/`.
3. **Si dos flujos comparten una pantalla** (ej. todos pasan por login antes de hacer lo suyo), reusen la misma clase — no la reescriban.

Este es el criterio que vas a ver aplicado en el resto de la documentación: `04-buenas-practicas.md` profundiza en cómo elegir selectores dentro de cada Page Object, y `08-correr-un-test-existente.md` / `09-datos-de-test-profesionales.md` muestran cómo se ve un test ya armado con este patrón en la práctica.
