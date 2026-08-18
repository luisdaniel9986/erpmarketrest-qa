# Errores comunes y cómo resolverlos

Referencia rápida de errores que ya nos aparecieron trabajando en este repo. Buscá el mensaje que te tira la terminal y andá directo a la sección.

## `Fatal error in launcher: Unable to create process using '"...\venv\Scripts\python.exe" ...'`

**Causa:** el `venv` se creó en una carpeta y después la carpeta del proyecto se movió o renombró. Los `.exe` de `venv\Scripts\` (`pytest.exe`, `pip.exe`, `playwright.exe`) tienen la ruta al intérprete grabada de forma fija al crearse — no se actualiza sola al mover la carpeta.

**Fix:** recrear el venv en la ubicación actual. No hay forma de "reparar" el venv movido, hay que rehacerlo:

```bash
deactivate
rmdir /s /q venv          # o: Remove-Item -Recurse -Force venv
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
```

## `pytest: error: unrecognized arguments: -tracing`

**Causa:** typo — un solo guion (`-tracing`) en vez de doble guion (`--tracing`). Le pasa a cualquiera al escribir rápido.

**Fix:**
```bash
pytest --tracing on tests/test_login.py
```

## `playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded` justo después de un login

**Causa típica:** condición de carrera. `LoginPage.login()` hace clic en "Iniciar Sesión" pero no espera a que termine la redirección antes de que el código siguiente navegue a otra URL con `.goto(...)`. Ese `goto()` se dispara antes de que la sesión quede establecida, la app te devuelve a `/login`, y el selector que buscabas en la otra pantalla nunca aparece — de ahí el timeout.

**Fix:** después de loguear y antes de navegar a la siguiente pantalla, esperá explícitamente a que el login haya terminado:

```python
login_page.login(credenciales["email"], credenciales["password"])
expect(page).to_have_url(re.compile(r"/dashboard"))   # <- esta línea evita la carrera
```

Ver el ejemplo completo en `tests/test_categoria.py`.

## Un `<select>` no responde a `get_by_label(...)` (o el test no logra abrirlo/seleccionarlo)

**Causa:** varios selects del sistema (Categoría, Marca, Almacén, Estado, etc.) están mejorados con TomSelect, que oculta el `<select>` original y lo reemplaza por su propio HTML. Aunque el campo tenga un label bien puesto, no es el elemento que un usuario (ni Playwright) termina clickeando.

**Fix:** usar el `data-testid` que ya tiene puesto ese campo, en vez de `get_by_label`:

```python
page.get_by_test_id("product-category").click()
page.get_by_text("BEBIDAS").click()
```

Detalle completo en `04-buenas-practicas.md`.

## `Failed: Faltan QA_EMAIL / QA_PASSWORD. Copia .env.example a .env y completa tus credenciales de prueba.`

**Causa:** no existe un archivo `.env` en la raíz del proyecto (o existe pero está vacío / mal completado). La fixture `credenciales` en `conftest.py` lee esas variables y falla el test a propósito si no las encuentra, para no dejar avanzar un test con credenciales vacías.

**Fix:**
```bash
cp .env.example .env
```
Y completá `QA_EMAIL` / `QA_PASSWORD` con tu usuario de prueba real dentro de `.env`.

## El editor (VS Code / Pylance) marca `Import "playwright.sync_api" could not be resolved`

**Causa:** no es un error real — el test corre bien igual con `pytest`. Es que el editor no tiene seleccionado el intérprete de Python del `venv` del proyecto, entonces no encuentra los paquetes instalados ahí para el autocompletado.

**Fix (VS Code):** `Ctrl+Shift+P` → "Python: Select Interpreter" → elegir el que apunta a `venv\Scripts\python.exe` dentro de la carpeta del proyecto.

## No encontrás tu error acá

Si te aparece algo que no está en esta lista y lo resolviste (o alguien te ayudó a resolverlo), agregalo acá siguiendo el mismo formato: el mensaje textual como título, causa, fix. Así no lo volvemos a investigar desde cero la próxima vez.
