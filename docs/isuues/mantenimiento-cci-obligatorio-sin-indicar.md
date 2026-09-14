---
name: Reporte de bug
about: Un fallo encontrado probando el sistema
title: "[Mantenimiento][Cuentas Bancarias] El campo CCI es obligatorio en el backend pero no se marca como requerido, y el error no muestra ningún toast"
labels: bug
---

## Módulo

mantenimiento (Cuentas Bancarias)

## Severidad

- [ ] Critical — bloquea el flujo, no hay forma de continuar
- [x] Major — funciona pero con un comportamiento incorrecto
- [ ] Minor — cosmético, no bloquea nada

## Pasos para reproducir

1. Ir a `/mantenimiento/cuentas/index`.
2. Clic en "Nueva Cuenta".
3. Completar Nombre, Titular, Moneda, Banco y N° Cuenta — **sin** completar el campo "CCI" (su label no tiene asterisco/indicador de obligatorio, a diferencia de los demás campos requeridos del formulario).
4. Clic en "Registrar" y confirmar "SÍ, REGISTRAR" en el diálogo de confirmación.

## Resultado esperado

O bien el campo CCI se guarda como opcional (como su label sugiere), o si el backend realmente lo exige, el formulario debería marcarlo visualmente como obligatorio (mismo estilo `required_field` que Nombre/Titular/Moneda/Banco/N° Cuenta) y mostrar una notificación toast de error indicando que falta un campo — igual que hace el resto de la app ante cualquier otro error de validación (`toastr.error(...)` se dispara en el `catch` para cualquier error que no sea 422 de validación).

## Resultado real

El backend rechaza la creación con "El CCI es obligatorio." (HTTP 422), pero:
- El label "CCI" no tiene el estilo `required_field` — nada en el formulario indica que es obligatorio antes de enviarlo.
- El bloque `catch` de `submit()` en `CreateBankAccountModal.vue` entra a la rama `err.response?.status === 422`, asigna el error al campo y hace `return` — **nunca llama a `toastr.error(...)`**. El modal de carga ("Registrando...") se cierra y el modal de creación queda abierto sin ningún aviso visible más que un pequeño texto rojo debajo del campo CCI.
- Un usuario que no repare en ese texto pequeño puede pensar que el botón "Registrar" simplemente no hizo nada.

## URL exacta

https://test-inventario.marketcode.store/mantenimiento/cuentas/index

## Usuario / datos usados

Usuario admin de prueba (`admin@gmail.com`). No depende de datos específicos, reproducible con cualquier cuenta bancaria nueva sin CCI.

## Evidencia

Encontrado mientras se automatizaba `tests/maintenance/test_bank_account.py`. Confirmado con un script de diagnóstico aparte que inspeccionó la respuesta 422 y el DOM tras el submit — el mensaje `El CCI es obligatorio.` aparece únicamente como `.invalid-feedback` bajo el input `#bank-account-cci`, sin toast.

Archivo de referencia del componente: `resources/js/Pages/Tenant/Maintenance/BankAccount/components/CreateBankAccountModal.vue` — label del campo CCI en la línea ~48 (sin `required_field`), manejo del catch 422 en la función `submit()` (líneas ~191-197, sin `toastr.error`).

## Test relacionado (si aplica)

`tests/maintenance/test_bank_account.py::test_crear_cuenta` — el Page Object (`pages/maintenance/bank_account_page.py::crear_cuenta`) ahora completa el CCI siempre para poder crear la cuenta; se dejó un comentario ahí mismo referenciando este issue.
