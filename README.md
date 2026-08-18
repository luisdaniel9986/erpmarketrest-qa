# erpmarketrest-qa

Tests automatizados (Playwright + pytest) para el ERP. Este repo es de testing — no requiere acceso al código fuente del sistema, solo interactúa con la aplicación ya corriendo, igual que lo haría un usuario desde el navegador.

## Empezar

Si es tu primera vez en este repo, seguí `docs/` en este orden:

| # | Doc | Qué encontrás |
|---|---|---|
| 01 | [`01-instalacion.md`](docs/01-instalacion.md) | Clonar el repo, crear el venv, instalar Playwright |
| 02 | [`02-guia-testing.md`](docs/02-guia-testing.md) | Tu primer test (login), cómo depurar un fallo con tracing |
| 03 | [`03-patron-de-diseno.md`](docs/03-patron-de-diseno.md) | El patrón de diseño del proyecto (Page Object Model) — leelo antes de escribir un test nuevo |
| 04 | [`04-buenas-practicas.md`](docs/04-buenas-practicas.md) | Cómo elegir selectores, credenciales, dividir trabajo en equipo, qué no hacer |
| 05 | [`05-comandos.md`](docs/05-comandos.md) | Referencia rápida de comandos (correr tests, depurar, git) |
| 06 | [`06-ejemplo-issue.md`](docs/06-ejemplo-issue.md) | Ejemplo de un bug bien reportado en GitHub Issues |
| 07 | [`07-codegen-y-auth.md`](docs/07-codegen-y-auth.md) | Grabar flujos nuevos con Codegen, y manejo de sesión (`auth.json`) |
| 08 | [`08-correr-un-test-existente.md`](docs/08-correr-un-test-existente.md) | Cómo correr un test ya escrito, y por qué no es "un script para crear lo que quiera" |
| 09 | [`09-datos-de-test-profesionales.md`](docs/09-datos-de-test-profesionales.md) | Nombres dinámicos, `@pytest.mark.parametrize`, limpieza de datos de test |
| 10 | [`10-auth-json-vs-login-en-tests.md`](docs/10-auth-json-vs-login-en-tests.md) | Por qué los tests se loguean solos y no reusan `auth.json` |
| 11 | [`11-errores-comunes.md`](docs/11-errores-comunes.md) | Troubleshooting: errores ya vistos y su solución |

## Quick start

```bash
git clone https://github.com/luisdaniel9986/erpmarketrest-qa.git
cd erpmarketrest-qa
python -m venv venv
venv\Scripts\activate          # Windows — Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env           # completá QA_EMAIL / QA_PASSWORD

pytest                         # correr toda la suite
```

Si algo de esto falla, revisá primero `docs/11-errores-comunes.md`.

## Estructura del proyecto

```
erpmarketrest-qa/
├── pages/          ← un archivo por pantalla del sistema (Page Object Model)
├── tests/          ← los tests, organizados por flujo/funcionalidad
├── conftest.py      ← fixtures compartidas (ej. credenciales)
├── pytest.ini       ← configuración (base_url del entorno de pruebas)
└── docs/            ← toda la documentación, ver tabla arriba
```
