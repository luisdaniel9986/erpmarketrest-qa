# Instalación del entorno de testing

Esta guía es para el equipo de testing externo. No necesitas acceso al código fuente del sistema — todo lo que vas a hacer es escribir scripts que interactúan con la aplicación ya corriendo, igual que lo haría un usuario desde el navegador.

## Requisitos previos

- Python 3.8 o superior instalado (`python --version` para verificar).
- `pip` disponible (viene con Python).

## Paso 1: clonar el repo y crear un entorno aislado

```bash
git clone https://github.com/luisdaniel9986/erpmarketrest-qa.git
cd erpmarketrest-qa
python -m venv venv
```

Activar el entorno virtual:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

Vas a ver `(venv)` al inicio de la línea de tu terminal cuando esté activo. Repetí este paso (`activate`) cada vez que abras una terminal nueva para trabajar en este proyecto.

**Importante:** la carpeta `venv/` es solo el entorno de Python (el intérprete y las librerías instaladas) — no pongas tus archivos de test ahí dentro. La estructura del proyecto es esta:

```
erpmarketrest-qa/
├── venv/                  ← el entorno, no lo tocás
├── .env                   ← tus credenciales de prueba (creás este archivo vos, no se sube a git)
├── .env.example           ← plantilla del archivo de arriba
├── pytest.ini             ← configuración (URL del entorno de pruebas)
├── conftest.py             ← datos compartidos entre tests (credenciales)
├── requirements.txt
├── pages/                  ← una clase por pantalla (Page Object Model)
│   └── login_page.py
└── tests/                  ← tus tests van acá
    └── test_login.py
```

## Paso 2: instalar Playwright

Con el venv activado:

```bash
pip install -r requirements.txt
playwright install
```

El segundo comando descarga los navegadores (Chromium, Firefox, WebKit) que Playwright va a controlar. Puede tardar unos minutos la primera vez.

## Paso 3: verificar que quedó instalado

```bash
playwright --version
```

Debería imprimir algo como `Version 1.4x.x`. Si ves eso, está listo.

Como chequeo extra, podés grabar un mini-test de prueba sin escribir código:

```bash
playwright codegen https://example.com
```

Se abre un navegador y una ventana con código Python que se genera solo mientras navegás. Cerrá ambas ventanas cuando confirmes que funciona — era solo para probar la instalación.

## Siguiente paso

Continuá con `02-guia-testing.md` para escribir y correr tu primer test real contra el sistema.
