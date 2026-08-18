# Correr un test que ya existe (ej. `test_categoria.py`)

## Cómo correrlo

Con el venv activado, desde la raíz del repo:

```bash
pytest tests/test_categoria.py
```

Eso corre `test_crear_categoria`: login → ir a Categorías → clic en "NUEVO" → completar nombre → Guardar → confirmar → verificar que aparece en la lista.

## Un test no es "un script para crear lo que yo quiera"

Es un error común al empezar: pensar que un archivo en `tests/` es una herramienta que hacés correr cada vez que necesitás crear algo real en el sistema, pasándole el dato que se te ocurra en el momento. **No es eso.**

Un test es una **verificación automatizada y repetible** de que un flujo funciona. Por diseño:

- Corre siempre igual, sin intervención humana en el medio.
- Se corre una y otra vez (en tu máquina, en la de un compañero, en CI) y tiene que dar el mismo resultado cada vez.
- Su objetivo es detectar si algo se rompió, no operar el sistema para lograr un resultado de negocio.

Si tu intención real es **crear categorías reales porque las necesitás para otra cosa** (cargar datos, preparar un ambiente, etc.), eso es un caso de uso distinto — un script operativo, no un test — y no correspondería a este repo de QA. Este repo es para verificar que el sistema funciona, no para operarlo.

## El problema concreto de `test_categoria.py` tal como está

Ahora mismo el nombre de la categoría está fijo en el código:

```python
categoria_page.crear_categoria("C3")
```

Consecuencia: si corrés el test dos veces, intenta crear `"C3"` dos veces. Si el sistema no permite nombres duplicados, la segunda corrida falla — no porque el flujo esté roto, sino porque el dato de prueba ya existe. Eso es un test mal escrito, no un bug real del sistema, y un QA tiene que saber distinguir esa diferencia antes de reportar algo como bug.

La solución (nombres dinámicos, parametrización, limpieza de datos) está en `09-datos-de-test-profesionales.md`.
