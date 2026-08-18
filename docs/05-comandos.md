# Comandos importantes (referencia rápida)

## Entorno

```bash
# activar el entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux

# instalar dependencias (primera vez o tras un git pull con cambios)
pip install -r requirements.txt
playwright install

# verificar instalación
playwright --version
```

## Correr tests

```bash
pytest                                    # toda la suite
pytest tests/test_login.py                # un archivo puntual
pytest tests/test_login.py::test_login_exitoso   # un test puntual
pytest -k "credenciales_invalidas"        # por nombre (coincidencia parcial)

pytest --headed                           # con navegador visible
pytest --headed --slowmo 500              # visible y lento, para seguir cada paso
pytest --base-url=https://otra-url.com    # contra otro entorno, sin tocar código
```

## Depurar un fallo

```bash
pytest --tracing on                       # genera trace en test-results/<test>/trace.zip
playwright show-trace test-results/<carpeta-del-test>/trace.zip   # abre la línea de tiempo

pytest --screenshot=only-on-failure       # guarda captura al fallar
pytest --video=retain-on-failure          # graba video, lo conserva solo si falla
```

Ver `02-guia-testing.md` → "Cuando un test falla" para el ejemplo completo con salida real.

## Escribir un test nuevo

```bash
playwright codegen https://tes1.marketcode.store   # graba clics y genera código Python
```

## Git (flujo de trabajo en equipo)

```bash
git checkout main
git pull origin main

git checkout -b feature/tests-facturacion   # una rama por dominio/flujo que estés probando

git add .
git commit -m "Agrega tests de facturación"
git push origin feature/tests-facturacion   # y después, Pull Request en GitHub
```

## Checklist antes de empezar a testear

- [ ] `venv` activado (`(venv)` visible en la terminal)
- [ ] `.env` completo con tus credenciales de prueba (`cp .env.example .env` si no existe)
- [ ] `pytest.ini` apunta al entorno correcto (`base_url`)
- [ ] `git pull origin main` reciente, por si hay tests nuevos de tu compañero
