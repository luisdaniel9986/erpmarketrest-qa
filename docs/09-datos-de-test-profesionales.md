# Datos de test: nombres dinámicos, parametrización y limpieza

Sigue de `08-correr-un-test-existente.md`. Ahí vimos el problema: `test_categoria.py` crea siempre `"C3"`, lo que rompe en la segunda corrida si el sistema no permite duplicados. Así lo resuelve un QA con experiencia.

## 1. Nombre único generado en cada corrida

En vez de un string fijo, generá un nombre que cambie cada vez que corre el test — así nunca choca con una corrida anterior:

```python
import time

def test_crear_categoria(page: Page, credenciales):
    nombre = f"Categoria QA {int(time.time())}"
    ...
    categoria_page.crear_categoria(nombre)
    expect(page.get_by_text(nombre)).to_be_visible()
```

`int(time.time())` da un número distinto cada segundo (ej. `1755461234`), así que el nombre final queda como `"Categoria QA 1755461234"` — único, sin coordinarte con nadie ni llevar cuenta manual de qué nombres ya se usaron.

## 2. Probar varios casos sin duplicar código: `@pytest.mark.parametrize`

Si además de "un nombre normal" querés cubrir otros casos (nombre con tildes, con caracteres especiales, un caso que debería fallar por estar vacío, etc.), no se escribe un `def test_...` distinto para cada uno. Se usa `parametrize`, y pytest corre el mismo test una vez por cada valor de la lista:

```python
import pytest

@pytest.mark.parametrize("nombre", ["Bebidas", "Lácteos", "Categoría Ñ"])
def test_crear_categoria(page: Page, credenciales, nombre):
    login_page = LoginPage(page)
    login_page.ir_a_login()
    login_page.login(credenciales["email"], credenciales["password"])
    expect(page).to_have_url(re.compile(r"/dashboard"))

    categoria_page = CategoriaPage(page)
    categoria_page.ir_a_categorias()
    categoria_page.crear_categoria(nombre)
    expect(page.get_by_text(nombre)).to_be_visible()
```

Esto corre como 3 tests independientes: `test_crear_categoria[Bebidas]`, `test_crear_categoria[Lácteos]`, `test_crear_categoria[Categoría Ñ]`. Si uno falla, ves exactamente cuál, sin que te tape a los otros dos.

Nota: acá los tres valores son fijos otra vez (no dinámicos) — si vas a correr esto muchas veces, combiná esto con el punto 1 (ej. `f"{nombre} {int(time.time())}"` dentro del test) para que tampoco choquen entre corridas.

## 3. La pregunta que hay que hacerle al equipo de dev: ¿el ambiente se limpia solo?

Cada test que crea datos (categorías, productos, notas, lo que sea) dejá algo en el sistema. Si nada lo borra, el ambiente de pruebas se va llenando de basura con el tiempo: "Categoria QA 1755461234", "Categoria QA 1755461500", etc., cada vez que alguien corre la suite.

Esto no es solo estética — puede llegar a:
- Hacer lento o confuso el ambiente para todo el equipo (listas larguísimas, difícil encontrar datos reales de prueba).
- Ensuciar métricas o reportes si alguien mira ese ambiente asumiendo que los datos son reales.

**Antes de automatizar más creación de datos, preguntale al equipo de desarrollo si existe un flujo para eliminar categorías** (o lo que sea que estés creando). Si existe, un test bien escrito hace *teardown*: crea el dato, verifica lo que tenga que verificar, y al final lo borra — para que la corrida no deje rastro.

Ejemplo de la idea (una vez que exista `CategoriaPage.eliminar_categoria(nombre)`):

```python
def test_crear_categoria(page: Page, credenciales):
    nombre = f"Categoria QA {int(time.time())}"
    ...
    categoria_page.crear_categoria(nombre)
    expect(page.get_by_text(nombre)).to_be_visible()

    categoria_page.eliminar_categoria(nombre)  # limpieza: no deja basura en el ambiente
```

Si todavía no existe esa función en `pages/categoria_page.py`, no la inventes ni la fuerces — primero confirmá con dev que el flujo de borrado existe y funciona, y ahí se agrega siguiendo el mismo patrón que `crear_categoria`.

## Siguiente paso

Si todavía no tenés claro por qué el test se loguea de nuevo en vez de reusar `auth.json`, ver `10-auth-json-vs-login-en-tests.md`.
