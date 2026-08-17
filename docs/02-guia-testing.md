# Guía de testing: tu primer test (login)

Antes de empezar, asegurate de haber completado `01-instalacion.md`.

## Datos de conexión

**1. URL del entorno de pruebas** — ya está configurada en `pytest.ini`, en la raíz del proyecto:

```ini
[pytest]
base_url = https://tes1.marketcode.store
testpaths = tests
```

Gracias a esto, los tests usan rutas relativas (`page.goto("/login")`) en vez de repetir la URL completa en cada uno. Si el equipo te da otro entorno para probar, no hace falta tocar código — corré `pytest --base-url=https://otra-url.com`.

**2. Credenciales de prueba** — van en un archivo `.env` en la raíz (nunca se sube a git, revisá que `.gitignore` lo tenga listado):

```bash
cp .env.example .env
```

Y completá `.env` con lo que te dé el equipo:

```
QA_EMAIL=usuario-prueba@tudominio.com
QA_PASSWORD=password-de-prueba
```

No uses credenciales reales de clientes ni datos de producción. Si no tenés un usuario de prueba, pedilo antes de empezar.

## Tu primer test: login

El proyecto ya trae `pages/login_page.py`, una clase que encapsula los selectores de la pantalla de login (ver `03-buenas-practicas.md` para el porqué de este patrón). El test en sí queda corto — `tests/test_login.py`:

```python
import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_login_exitoso(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])

    expect(page).to_have_url(re.compile(r"/dashboard"))


def test_login_credenciales_invalidas(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], "password-incorrecta")

    expect(login_page.mensaje_error()).to_be_visible()
    expect(page).to_have_url(re.compile(r"/login"))
```

### Por qué está escrito así

- `credenciales` es una fixture definida en `conftest.py` — lee `QA_EMAIL`/`QA_PASSWORD` de tu `.env`, así nadie hardcodea contraseñas en el código que después se sube a git.
- `LoginPage` usa `get_by_label(...)` para los campos y `get_by_role("button", name=...)` para el botón — así es como un usuario real (o un lector de pantalla) identifica cada elemento, no dependemos de detalles internos de HTML.
- `expect(page).to_have_url(...)` confirma que, tras el login, el sistema redirigió a donde correspondía — esa es la señal real de éxito o fallo.

Para más detalle sobre por qué se eligen estos selectores en particular, ver `03-buenas-practicas.md`.

## Correr el test

Desde la raíz del proyecto (`erpmarketrest-qa/`), con el venv activado:

```bash
# toda la suite
pytest

# solo el archivo de login
pytest tests/test_login.py

# con el navegador visible, para ver qué está pasando
pytest --headed

# más lento, para seguir cada paso con la vista
pytest --headed --slowmo 500
```

Si todo salió bien, vas a ver `2 passed` en la terminal.

## Cuando un test falla: cómo depurarlo

Primero, mirá el mensaje de error en la terminal — Playwright incluye un "Aria snapshot" (una foto del HTML en el momento del fallo) que muchas veces ya te dice qué pasó, sin necesitar nada más. Por ejemplo, si el login falla porque las credenciales están mal, ahí vas a ver algo como `listitem: These credentials do not match our records.`

Si con eso no alcanza, corré con tracing activado:

```bash
pytest tests/test_login.py --tracing on
```

Esto genera un `trace.zip`, pero **no** queda suelto en la carpeta — Playwright lo guarda dentro de `test-results/<nombre-del-test>/trace.zip`. Para verlo:

```bash
playwright show-trace test-results/tests-test-login-py-test-login-exitoso-chromium/trace.zip
```

(El nombre exacto de la carpeta lo arma Playwright a partir del archivo y el test — después de que falle un test, hacé `dir test-results` / `ls test-results` para ver el nombre real, o simplemente arrastrá el `trace.zip` que encuentres ahí a `playwright show-trace <ruta>`.)

Se abre una ventana con: una línea de tiempo de cada acción del test, captura de pantalla antes/después de cada una, la pestaña **Console** (errores de JS), **Network** (requests/responses — útil para distinguir un bug del backend de un problema del test) y **Source** (la línea exacta de tu código que falló). Es la forma más rápida de entender qué pasó sin repetir la prueba a mano.

La carpeta `test-results/` se regenera en cada corrida — está en `.gitignore`, no se sube al repo.

## Escribir tests para otros flujos

No hace falta escribir todo a mano. Podés grabar la interacción y generar el código automáticamente:

```bash
playwright codegen https://tu-staging.tudominio.com
```

Navegá el flujo que querés probar (crear un comprobante, buscar un producto, etc.) y copiá el código Python generado como punto de partida. Después:

1. Ajustalo para que use `get_by_label` / `get_by_role` donde se pueda, siguiendo el mismo criterio que en el ejemplo de login.
2. Movés los selectores a una clase nueva en `pages/` (ej. `pages/facturacion_page.py`), siguiendo el mismo patrón que `pages/login_page.py`.
3. El test que llama a esa clase va en `tests/` (ej. `tests/test_facturacion.py`).

Ver `03-buenas-practicas.md` para el criterio completo de organización — importante si van a trabajar dos personas sobre el mismo repo.
