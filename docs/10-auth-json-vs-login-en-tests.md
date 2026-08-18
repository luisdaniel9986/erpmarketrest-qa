# Por qué los tests no reusan `auth.json`

Duda frecuente al empezar: "ya generé `auth.json` con Codegen, ¿por qué `test_categoria.py` se loguea de nuevo con `LoginPage.login()` en vez de usar ese archivo?". Tiene sentido la confusión porque ambos terminan logueando — pero son dos flujos separados que no se tocan entre sí. Ver también `07-codegen-y-auth.md` para el contexto de qué es `auth.json` y cómo se genera.

## Dos caminos distintos, mismo destino (`/login`), propósitos distintos

**`auth.json` → es solo para vos, cuando grabás con Codegen.** Lo generás una vez para no tener que loguearte a mano cada vez que abrís el grabador a capturar un flujo nuevo. Es una comodidad para el momento de *escribir* el test, nada más.

**`test_categoria.py` (y cualquier test) → nunca lee `auth.json`.** Cuando el test corre, hace login de verdad con `LoginPage.login()` y las credenciales de tu `.env` (vía la fixture `credenciales`), en cada corrida. No hay `storage_state` ni `auth.json` en ningún lado de `pages/login_page.py` ni de los tests.

## Por qué el test no reusa la sesión guardada, aunque técnicamente podría

Tres razones concretas:

1. **`auth.json` expira.** Es una sesión con tiempo de vida limitado (cookies/tokens). Si el test dependiera de ese archivo, andaría bien un par de días y después empezaría a fallar random cuando la sesión venza — un error confuso si no te acordás que ese archivo existe y que tiene fecha de vencimiento.

2. **El test tiene que poder correr en cualquier lado, sin pasos manuales previos.** Si un compañero de QA clona el repo, o corre en un pipeline de CI, no va a tener tu `auth.json` — es personal, nunca se comparte ni se commitea (ver `07-codegen-y-auth.md`). Pero sí va a tener sus propias credenciales en su `.env`. Que el test se loguee solo garantiza que funciona en cualquier máquina, sin preparación extra ni archivos que alguien tenga que pasarte a mano.

3. **El login en sí es parte de lo que estás verificando indirectamente.** Si el login se rompe, es mejor que los tests que dependen de él (como crear una categoría) también fallen — es una señal de alerta real. Si en cambio reusaras una sesión vieja ya autenticada, un login roto podría pasar desapercibido durante días.

## Resumen

| | `auth.json` | `LoginPage.login()` en tests |
|---|---|---|
| Para qué sirve | Grabar más rápido con Codegen | Autenticarse en cada corrida de test |
| Quién lo usa | Vos, a mano, con el Inspector | El test, automáticamente |
| Se comparte con el equipo | No, nunca | No aplica — cada QA usa su `.env` |
| Qué pasa si expira | Volvés a generarlo (`--save-storage`) | No aplica, no depende de ningún archivo guardado |

Son caminos paralelos que coinciden en el mismo lugar (`/login`) pero sirven a momentos distintos del trabajo: uno es una herramienta tuya para grabar, el otro es cómo el test real se autentica, siempre, de forma repetible.
