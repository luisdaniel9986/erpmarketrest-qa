# Generar tests con Codegen, y manejo de sesión (`auth.json`)

## Qué es Codegen

`playwright codegen` es un grabador: abrís un navegador de verdad, hacés clic/escribís como un usuario normal, y Playwright va escribiendo el código Python de cada acción en una ventana aparte (el Inspector). No hace falta escribir selectores a mano — los copiás de ahí y después los acomodás al patrón del proyecto (Page Object Model, ver `03-patron-de-diseno.md`).

```bash
playwright codegen https://tes1.marketcode.store
```

## El problema: el sistema requiere login

Si abrís codegen directo en una pantalla interna (ej. Categorías), te va a redirigir a `/login` porque no hay sesión. Dos formas de resolverlo:

**Opción rápida (una sola vez, sesión se pierde al cerrar):** loguearte a mano dentro de la misma grabación antes de ir a la pantalla que te interesa. Sirve, pero repetís el login cada vez que grabás algo nuevo.

**Opción recomendada: guardar la sesión en un archivo (`auth.json`) y reusarla.**

### 1. Grabar el login una vez y guardar la sesión

```bash
playwright codegen --save-storage=auth.json https://tes1.marketcode.store/login
```

Se abre el navegador, hacés login con tu usuario de prueba, cerrás la ventana. Esto crea `auth.json` en la carpeta actual con las cookies/tokens de esa sesión.

### 2. Reusar esa sesión para grabar cualquier pantalla, ya logueado

```bash
playwright codegen --load-storage=auth.json https://tes1.marketcode.store/inventario/categorias/index
```

Arrancás directo en la pantalla, sin pasar por login. Ahí hacés el flujo real (clic en "Nuevo", completar el formulario, guardar) y copiás el código generado.

### Ejemplo: grabar la creación de una categoría

Con `auth.json` ya generado (paso 1), corrés el paso 2 apuntando a `/inventario/categorias/index`, hacés:

1. Clic en "NUEVO"
2. Completar "Nombre de la categoría"
3. Clic en "Guardar"
4. Confirmar en el diálogo ("Sí")

Codegen te va a dejar algo parecido a esto (crudo, tal cual sale del Inspector):

```python
page.get_by_role("button", name=" NUEVO").click()
page.get_by_role("textbox", name="Nombre de la categoría").fill("C2")
page.get_by_role("button", name=" Guardar").click()
page.get_by_role("button", name="Sí").click()
```

Eso **no se pega directo en `tests/`** — se convierte al patrón del proyecto, igual que `login_page.py`:

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

`tests/test_categoria.py`:
```python
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.categoria_page import CategoriaPage


def test_crear_categoria(page: Page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])

    categoria_page = CategoriaPage(page)
    categoria_page.ir_a_categorias()
    categoria_page.crear_categoria("C2")

    expect(page.get_by_text("C2")).to_be_visible()
```

Nota: el test final vuelve a loguearse con la fixture `credenciales` en vez de depender de `auth.json` — `auth.json` es solo una herramienta para grabar más rápido con codegen, no algo que se usa dentro de los tests ya escritos.

## `auth.json`: reglas para todo el equipo de QA

**`auth.json` es personal, nunca se comparte ni se sube al repo.** Es literalmente tu sesión activa (cookies/tokens) — quien tenga el archivo puede actuar como ese usuario logueado, sin necesitar la contraseña. Es tan sensible como tu `.env`.

Por qué importa que sea personal y no un archivo único compartido entre todos los QA:

- **Riesgo de "cruce" de sesiones:** si dos personas usan el mismo `auth.json` (mismo usuario) y corren algo en paralelo, muchos sistemas invalidan la sesión anterior al detectar un login nuevo — a uno se le corta la sesión sin aviso, en medio de una grabación o corrida.
- **Trazabilidad:** si algo raro pasa en el entorno de pruebas, es mejor poder saber qué usuario lo generó.

Reglas concretas:

1. **Cada QA genera su propio `auth.json` localmente**, con su propio usuario de prueba (o al menos credenciales separadas de las de sus compañeros).
2. **Nunca lo commitees.** Ya está agregado a `.gitignore` (ver más abajo) — si por algún motivo `git status` te lo muestra como "untracked" y a punto de subirse, pará y avisá antes de hacer `git add`.
3. **No lo mandes por chat/email/Slack.** Si necesitás compartir cómo reproducir algo, compartí los *pasos*, no el archivo de sesión.
4. Es un archivo **descartable**: si expira, da error raro, o simplemente querés limpiar, borralo y volvé a generarlo con el paso 1. No hay que "cuidarlo".

### Cómo lo hacen los equipos de QA más grandes (para referencia)

En vez de un `auth.json` generado a mano una vez y reusado por semanas, los equipos con más tests automatizan ese primer login como parte de la propia suite: un fixture de pytest (scope `session`) hace login una sola vez al arrancar la corrida completa, guarda el `storage_state` en un archivo temporal, y todos los tests de esa corrida lo reusan — así no repiten el login en cada test y tampoco dependen de un archivo viejo guardado a mano. El archivo se genera de nuevo en cada corrida y se descarta al terminar.

Es un paso más de automatización que no hace falta ahora mismo con la suite actual, pero si el número de tests crece y el login empieza a hacerse lento, avisen y lo armamos.

## Siguiente paso

Con esto ya podés grabar cualquier flujo nuevo del sistema. Para dudas de cómo elegir selectores o dónde va cada cosa (Page Object, tests, etc.), volvé a `04-buenas-practicas.md`.

Si te queda dando vueltas la diferencia entre `auth.json` y el login que hace el test automatizado, ver `10-auth-json-vs-login-en-tests.md`.
