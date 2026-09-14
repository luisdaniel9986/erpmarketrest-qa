---
name: Reporte de bug
about: Un fallo encontrado probando el sistema
title: "[Menú][Platos] Editar un plato falla siempre — 'The PUT method is not supported for route menu/platos/{id}'"
labels: bug
---

> **✅ YA CORREGIDO** — verificado el 3 de septiembre de 2026: `tests/supply/test_plato.py::test_editar_plato` ahora pasa contra `test-inventario.marketcode.store`, y `routes/tenant/supply/web.php` ya registra la ruta como `Route::put('{id}', ...)`. Queda este archivo como referencia del hallazgo original — no hace falta subirlo a GitHub como issue nuevo, salvo que quieras dejarlo documentado igual con este estado.

## Módulo

menu (Platos / Dish)

## Severidad

- [x] Critical — bloquea el flujo, no hay forma de continuar
- [ ] Major — funciona pero con un comportamiento incorrecto
- [ ] Minor — cosmético, no bloquea nada

## Pasos para reproducir

1. Ir a `/menu/platos`.
2. Crear un plato cualquiera (o usar uno existente).
3. Desde el listado, abrir sus opciones y clic en "Editar".
4. Cambiar cualquier dato (por ejemplo el nombre) y clic en "Guardar".
5. Confirmar "Sí" en el diálogo de confirmación ("¿Actualizar plato?").

## Resultado esperado

El plato se actualiza y el sistema redirige de vuelta a `/menu/platos` mostrando el dato editado.

## Resultado real

La edición **nunca se guarda**: aparece un toast "ERROR EN LA PETICIÓN" con el mensaje del servidor:

> The PUT method is not supported for route menu/platos/{id}. Supported methods: POST, DELETE.

La página se queda en `/menu/platos/{id}/edit`. **Es 100% reproducible, siempre falla** — no depende de datos ni de condiciones particulares. Editar un plato está roto para cualquier usuario.

## Causa (verificada en el código)

Desajuste entre el formulario y la ruta registrada:

- `resources/js/Pages/Tenant/Supply/Dish/components/DishFormPage.vue` (función `buildFormData`, línea ~238) agrega `fd.append('_method', 'PUT')` cuando `mode === 'edit'` — el spoofing de método estándar de Laravel, que se usa junto a `axios.post(...)`.
- Pero `routes/tenant/supply/web.php` (línea ~25) registra esa ruta como `Route::post('{id}', [DishController::class, 'update'])->name('tenant.menu.platos.update')` — **POST**, no **PUT**.
- El middleware `MethodOverride` de Laravel toma el `_method=PUT` del form-data y reescribe el método efectivo de la petición a PUT antes de que llegue al router, pero el router solo tiene una ruta POST registrada en esa URI — de ahí el `MethodNotAllowedHttpException`.

Arreglo esperado: o cambiar la ruta a `Route::put('{id}', ...)` (manteniendo el `_method=PUT` del form), o quitar el `fd.append('_method', 'PUT')` del frontend (ya que de por sí usa `axios.post`). Cualquiera de las dos alcanza, hay que elegir una y que ambos lados coincidan.

## URL exacta

https://test-inventario.marketcode.store/menu/platos/{id}/edit

## Usuario / datos usados

Usuario admin de prueba (`admin@gmail.com`). No depende de datos específicos — reproducible editando cualquier plato.

## Evidencia

Encontrado automatizando `tests/supply/test_plato.py::test_editar_plato` — el test queda en rojo a propósito (no se debilitó la aserción) porque refleja el bug real; no es un problema del test. Confirmado además con un script de diagnóstico aparte que capturó el toast de error tal cual lo ve un usuario real.

Trace + video generados corriendo `pytest tests/supply/test_plato.py::test_editar_plato --tracing on --video on`:
- `test-results/tests-supply-test-plato-py-test-editar-plato-firefox/trace.zip`
- `test-results/tests-supply-test-plato-py-test-editar-plato-firefox/video.webm`

(Carpeta `test-results/` no se sube al repo — está en `.gitignore` y se regenera en cada corrida, ver `docs/02-guia-testing.md`. Arrastrá estos dos archivos directamente al cuerpo del issue en GitHub al crearlo.)

## Test relacionado (si aplica)

`tests/supply/test_plato.py::test_editar_plato` — queda fallando intencionalmente hasta que se corrija este bug.
