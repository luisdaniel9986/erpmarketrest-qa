# Ejemplo de un issue bien llenado

Esto **no es un bug real** — es un ejemplo inventado para que veas cómo se completa el template de `.github/ISSUE_TEMPLATE/bug_report.md` al abrir un issue nuevo en GitHub. Cuando reportes un bug de verdad, el formulario te va a aparecer con estos mismos campos vacíos.

---

**Título:** `[Login] El ícono de mostrar contraseña no cambia al hacer clic`

## Módulo

login

## Severidad

- [ ] Critical — bloquea el flujo, no hay forma de continuar
- [x] Major — funciona pero con un comportamiento incorrecto
- [ ] Minor — cosmético, no bloquea nada

## Pasos para reproducir

1. Ir a `/login`.
2. Escribir cualquier texto en el campo Contraseña.
3. Hacer clic en el ícono del ojo (a la derecha del campo).
4. Hacer clic de nuevo en el mismo ícono.

## Resultado esperado

El campo debería alternar entre mostrar el texto en claro y ocultarlo (`type="text"` / `type="password"`), y el ícono debería cambiar de ojo abierto a ojo tachado en cada clic.

## Resultado real

El campo sí alterna correctamente entre texto visible y oculto, pero el ícono se queda siempre en "ojo abierto" — no cambia a "ojo tachado" cuando la contraseña está visible.

## URL exacta

https://tes1.marketcode.store/login

## Usuario / datos usados

Usuario de prueba (`admin@gmail.com`), cualquier password de prueba — el bug no depende de las credenciales.

## Evidencia

Screenshot adjunto: antes y después del clic, se ve el mismo ícono en ambos casos.
(En un reporte real: arrastrá la imagen o el `.zip` del trace directamente al cuerpo del issue en GitHub — se sube solo.)

## Test relacionado (si aplica)

Ninguno todavía — se encontró probando manualmente. Si se agrega un test automatizado para esto, se referenciaría acá como `tests/test_login.py::test_toggle_password_icono`.

---

## Por qué este ejemplo es "bueno"

- El título dice módulo + qué falla, en una línea — se entiende sin abrir el issue.
- "Esperado" vs. "real" están separados y son específicos, no un genérico "no funciona".
- Los pasos son numerados y reproducibles por cualquiera, no "hice login y vi el error".
- No incluye credenciales reales ni datos de clientes.
