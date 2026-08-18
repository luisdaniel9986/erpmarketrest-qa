# Buenas prácticas de testing

## Cómo elegir un selector (locator)

Playwright ofrece varias formas de encontrar un elemento en la página. No todas son igual de buenas — hay una jerarquía recomendada, de mejor a peor:

1. **`get_by_role("button", name="...")`** — primera opción siempre que se pueda. Busca por el rol del elemento (botón, link, checkbox, etc.) y su texto visible, igual que lo percibiría un usuario real o un lector de pantalla.
2. **`get_by_label("...")`** — la mejor opción específicamente para campos de formulario. Busca el input a través del texto de su etiqueta.
3. **`get_by_placeholder(...)` / `get_by_text(...)`** — cuando no hay un rol o label claro disponible.
4. **`get_by_test_id("...")`** — **último recurso**. Busca por un atributo `data-testid` puesto a propósito para testing. Útil solo cuando no hay texto ni rol confiable (por ejemplo, un botón que es solo un ícono, o texto que cambia según el idioma).

### Por qué esta jerarquía y no ir directo a `data-testid`

Un test escrito con `get_by_role` o `get_by_label` verifica **dos cosas a la vez**: que el elemento funciona, y que está correctamente expuesto para accesibilidad (lectores de pantalla, navegación por teclado). Si un test así falla porque alguien rompió la etiqueta de un campo, esa falla es información real y valiosa.

Un test escrito con `get_by_test_id` **no detecta ese tipo de problema** — el testid vive pegado al elemento sin importar si está bien etiquetado o no. Por eso se usa como respaldo, no como primera opción, aunque exista disponible.

En el login del sistema, por ejemplo, el campo de contraseña y el de correo tienen labels correctamente asociados, así que se usa `get_by_label`. El botón "Iniciar Sesión" tiene texto visible, así que se usa `get_by_role`. Ninguno de los dos necesita `data-testid` — ese atributo queda disponible en el HTML como respaldo, pero no hace falta usarlo ahí.

## Casos especiales: cuando ni `getByLabel` ni `getByRole` alcanzan

El módulo de Inventory tiene dos situaciones donde ninguna de las opciones "normales" de la jerarquía funciona, y se resuelven con `data-testid` puesto a propósito:

### Selects mejorados con TomSelect

Casi todos los `<select>` del sistema (Categoría, Marca, Almacén, Estado, etc.) se mejoran en pantalla con una librería llamada TomSelect — la que convierte un select nativo en un combo con buscador. El problema para testing: TomSelect **oculta el `<select>` original** y lo reemplaza por su propio HTML. Aunque el campo tenga un `<label for="...">` bien puesto, `get_by_label(...)` no puede interactuar con el control real, porque el elemento que ve y clickea un usuario ya no es ese `<select>`.

Para estos campos, usá `get_by_test_id(...)` para abrir el combo, y después seleccioná la opción por su texto visible:

```python
page.get_by_test_id("product-category").click()
page.get_by_text("BEBIDAS").click()
```

Cada campo con TomSelect en el sistema ya tiene su `data-testid` puesto (ej. `product-category`, `product-brand`, `warehouse-branch`, `note-income-warehouse`, `kardex-product`, los filtros `*-status-filter` de cada listado, etc.) — inspeccioná el elemento en el navegador si no estás seguro del nombre exacto.

### Inputs generados por SweetAlert2 (ventanas de confirmación)

Algunas acciones (ej. "Dar de baja" en Productos por Vencer) abren un cuadro de diálogo con un input adentro, generado por una librería de alertas (SweetAlert2) en vez de ser parte del formulario normal de la página. Ahí tampoco hay `<label>` posible. Se resuelve igual, con `data-testid`:

```python
page.get_by_test_id("baja-cantidad-input").fill("5")
```

## Page Object Model: no repitas selectores en cada test

En vez de escribir `page.get_by_label(...)` suelto dentro de cada test, se agrupan los selectores de cada pantalla en una clase, dentro de `pages/`. Ejemplo real del proyecto, `pages/login_page.py`:

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

Y el test, en `tests/`, queda corto y se lee como una historia:

```python
def test_login_exitoso(page, credenciales):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))
```

Ventaja concreta: si mañana el botón "Iniciar Sesión" cambia de texto, arreglás una sola línea en `LoginPage`, no cada test que lo usa. Para un flujo nuevo, creá `pages/<flujo>_page.py` siguiendo este mismo patrón.

## Credenciales: nunca hardcodeadas

Las credenciales de prueba (`QA_EMAIL`, `QA_PASSWORD`) viven en tu `.env` local, no en el código. La fixture `credenciales` en `conftest.py` las lee automáticamente — cualquier test que las necesite solo pide `credenciales` como parámetro, como en el ejemplo de arriba. `.env` está en `.gitignore`: si alguna vez ves credenciales reales en un archivo que estás por commitear, pará y avisá antes de subirlo.

## Cómo dividir el trabajo entre testers

Con dos o más personas en el mismo repo, para no pisarse:

- **Un tester = un dominio funcional**. Por ejemplo: una persona se encarga de `pages/facturacion_page.py` + `tests/test_facturacion.py`, la otra de `pages/inventario_page.py` + `tests/test_inventario.py`.
- **Rama por feature**, nunca commitear directo a `main`: `git checkout -b feature/tests-facturacion`.
- **Pull request antes de mergear**, aunque sean solo dos personas — el otro revisa que el test tenga sentido y no rompa nada existente.
- Si dos tests necesitan la misma pantalla (ej. ambos flujos pasan por login), reusen la misma clase en `pages/` en vez de que cada uno escriba la suya.

## Qué NO hacer

- **No corras pruebas de carga o estrés** (muchos requests simultáneos, loops agresivos) sin avisar antes al equipo — podés afectar el entorno para otros testers o generar alertas innecesarias.
- **No compartas las credenciales de prueba** fuera del equipo de testing, ni las subas a repositorios públicos o herramientas externas.
- **No uses ni modifiques datos reales** de clientes — si el entorno de pruebas tiene datos de producción por error, avisá inmediatamente en vez de seguir probando ahí.
- **No asumas que un test que pasó una vez sigue pasando siempre** — corré la suite completa antes de dar por buena una funcionalidad, sobre todo después de cambios grandes.

## Cómo reportar un bug encontrado

Los bugs se reportan como **Issues de GitHub en este mismo repo** (`erpmarketrest-qa`), nunca por chat suelto — así queda trazable, se puede asignar, etiquetar y linkear a un test o a un commit que lo arregle.

Al abrir un issue nuevo en GitHub vas a ver el template ya armado (`.github/ISSUE_TEMPLATE/bug_report.md`) con estos campos para completar:

1. **Módulo** y **severidad** (Critical / Major / Minor) — agregá también el label correspondiente.
2. **Pasos para reproducir**, lo más específico posible (qué usuario, qué datos, qué botones/campos).
3. **Resultado esperado** vs. **resultado real**.
4. **URL exacta** donde ocurrió.
5. **Evidencia**: el trace de Playwright si el fallo salió de un test automatizado (ver `02-guia-testing.md` para generarlo con `--tracing on`), o una captura/video si fue manual.
6. **Test relacionado**, si existe uno que lo detectó.

Ver `05-ejemplo-issue.md` para un ejemplo ya completado, con explicación de por qué está bien escrito.

## Organización de los tests

- Un archivo por flujo o funcionalidad en `tests/` (`test_login.py`, `test_facturacion.py`, etc.), con su clase correspondiente en `pages/`, no todo mezclado en un archivo gigante.
- Nombres de test descriptivos que digan qué se está verificando: `test_login_exitoso`, `test_login_credenciales_invalidas`, no `test_1`, `test_2`.
- Un test debería poder leerse de arriba a abajo y entenderse sin tener que saltar a otro archivo — la lógica de selectores va en `pages/`, el test solo orquesta y verifica.
