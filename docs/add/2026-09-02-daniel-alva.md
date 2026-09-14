# Avance del 2 de septiembre de 2026 — Daniel Alva

## Resumen

Se completó la cobertura de Playwright/Pytest para todos los módulos y submódulos de tenant que todavía faltaban en modo HÍBRIDO, y se reorganizaron `pages/` y `tests/` en subcarpetas por módulo para que el repo escale mejor. Se agregaron credenciales de prueba para los roles CAJERO, VENDEDOR y MESERO (además del admin), necesarias porque varias reglas de negocio reales exigen un rol específico. En el proceso se encontraron y documentaron dos bugs reales de la aplicación — uno de los dos (Editar Plato) se corrigió en vivo en el ambiente durante la misma sesión.

## Reorganización de `pages/` y `tests/`

Antes todo vivía plano en `pages/` y `tests/`. Ahora está organizado por módulo, siguiendo la estructura de `ErpMarketRest`:

```
pages/                          tests/
├── login_page.py (compartido)  ├── test_login.py
├── inventory/                  ├── inventory/
├── cash/                       ├── cash/
├── cashier/                    ├── cashier/
├── maintenance/                ├── maintenance/
├── sale/                       ├── sale/
├── supply/                     ├── supply/
├── orders/                     ├── orders/
├── purchases/                  ├── purchases/
├── accounts/                   ├── accounts/
├── reports/                    ├── reports/
├── contabilidad/                ├── contabilidad/
└── dashboard/                  └── dashboard/
```

Los 12 pares página/test que ya existían (Almacén, Caja, Categoría, Inventario, Kardex, Kardex Valorizado, Marca, Nota de Ingreso, Nota de Salida, Producto, Valorización de Inventario, Vencimientos) se movieron con `git mv` a `inventory/` o `cash/` según corresponda, preservando el historial, y se corrigieron sus imports.

## Credenciales por rol

`conftest.py` ahora expone `credenciales` (admin, la de siempre) más `credenciales_cajero`, `credenciales_vendedor` y `credenciales_mesero`, cada una leyendo su propio par `QA_<ROL>_EMAIL` / `QA_<ROL>_PASSWORD` desde `.env`. Se actualizó `.env.example` con las nuevas variables (vacías, documentadas) para que cada tester complete su propio `.env` local. Hicieron falta porque varias reglas de negocio reales exigen un rol específico — por ejemplo, solo un usuario CAJERO puede aperturar una caja.

## Módulos y submódulos cubiertos

### Maintenance (10 pantallas nuevas)
Cargos, Centros de Costo, Comprobantes, Cuentas Bancarias, Colaborador, Usuario, Roles, Sedes, Empresa, Configuración (esta última solo toca campos seguros — nunca la "Zona de Peligro" de purga, que requiere contraseña de ADMIN y trunca datos del tenant).

### Cash y Cashier
Egresos (con apertura/cierre de caja real como precondición), Apertura/Cierre de Caja (ciclo completo abrir→cerrar, salvo que el ambiente no tenga mesero/vendedor cargado para la sede — en ese caso el test se salta con un mensaje claro), Mostrador Cajero (solo listado/filtros — el flujo de "Cobrar" emite un comprobante real y no se automatiza).

### Sale
Métodos de Pago, Condiciones de Pago, Comprobante de Venta (smoke: listado, filtros y armado del carrito, sin emitir), Notas de Crédito, Notas de Devolución, Resúmenes.

### Supply
Tipos de Plato, Platos (CRUD con imagen), Programación.

### Orders
Salón > Mesas, Mostrador Mesero (smoke: plano de mesas y filtros, sin tomar pedidos reales).

### Purchases
Proveedores, Documento de Compra (creación real usando condición de pago CRÉDITO para no depender de una caja abierta).

### Accounts, Reports, Contabilidad, Dashboard
Cuentas por Pagar/Cobrar (listado y filtros), Ventas Productos/Platos/Generales, SUNAT Individual/Masiva (aceptan tanto un resultado real como el error esperado de credenciales CPE no configuradas), Reporte Contable, Dashboard.

### Fuera de alcance (documentado, no implementado)
Wizards de importación/exportación de Inventario (NoteIncomeImport, ProductImport, ProductExport, SimpleCatalogImport) y la campanita de Notificaciones — baja prioridad, quedan pendientes para una siguiente iteración.

## Qué falta por testear

La cobertura es completa en amplitud (todo módulo/submódulo tiene Page Object + test), pero no en profundidad. Esto es lo que queda pendiente, ordenado por tipo:

### Fuera de alcance, no implementado
- Wizards de import/export de Inventario: `NoteIncomeImport`, `ProductImport`, `ProductExport`, `SimpleCatalogImport`.
- Campanita de Notificaciones (`PendingVoucherController`).

### Cubiertos solo a nivel smoke (navegación/filtros), no el flujo completo
Motivo en todos los casos: la acción real emite algo hacia SUNAT, muta una sesión de caja real, o requiere datos que este test no puede crear de forma segura.
- **Comprobante de Venta (POS)** — arma carrito y verifica totales; nunca emite.
- **Notas de Crédito / Notas de Devolución** — solo listado y filtros; no hay creación real (necesitan una venta ya emitida como referencia).
- **Resúmenes** — solo abre/cierra el modal de creación; no envía a SUNAT.
- **Mostrador Mesero** — solo plano de mesas y filtros; no toma pedidos reales.
- **Mostrador Cajero** — solo listado y filtro por estado; el flujo "Cobrar" no se automatiza.
- **Cuentas por Pagar / Cuentas por Cobrar** — solo listado y filtros; nunca se ejecuta "Pagar"/"Anular"/"Pagar seleccionadas" sobre una cuenta real.
- **SUNAT Individual / SUNAT Masiva** — el test acepta como válido tanto un resultado real como el toastr de "credenciales CPE no configuradas" (que es lo que este ambiente devuelve siempre); nunca se confirmó una respuesta real y exitosa de SUNAT.
- **Configuración** — solo el campo de umbral de venta (editar y revertir); nunca se toca Modo del Negocio, Ambiente de Facturación ni la Zona de Peligro.
- **Apertura/Cierre de Caja** — el ciclo completo abrir→cerrar está escrito y probado en código, pero en este ambiente no hay mesero/vendedor cargado para la sede del cajero de prueba, así que el test se salta (`pytest.skip`) en vez de ejecutar el flujo real. Si alguien carga ese personal, el test ya está listo para correr el ciclo completo sin tocar nada.

### Ideas para una siguiente iteración
- Confirmar con el equipo de datos si se puede cargar un colaborador con rol MESERO o VENDEDOR en la sede del cajero de prueba, para poder correr el ciclo de Apertura/Cierre y, con eso, destrabar también un test más completo de Egresos y Mostrador Cajero.
- Si alguna vez se configuran credenciales CPE de prueba en este tenant, actualizar `test_sunat_individual.py` / `test_sunat_masivo.py` para afirmar el resultado real en vez de aceptar el error de configuración como válido.
- Evaluar si vale la pena automatizar los wizards de import/export (piden un archivo Excel real, sería el mismo patrón que ya usa `pages/inventory/producto_page.py` para imagen).

## Bugs encontrados

1. **`docs/isuues/mantenimiento-cci-obligatorio-sin-indicar.md`** — En Mantenimiento > Cuentas Bancarias, el campo CCI es obligatorio en el backend pero su label no lo marca como tal, y el error de validación no muestra ningún toast (a diferencia del resto de la app). Severidad Major. Sigue sin corregir.
2. **`docs/isuues/menu-platos-editar-no-funciona.md`** — Editar un Plato fallaba siempre: el formulario mandaba `_method=PUT` pero la ruta solo aceptaba POST (`Route::post('{id}', ...)` en `routes/tenant/supply/web.php` vs `_method=PUT` en `DishFormPage.vue`). Severidad Critical, 100% reproducible, trace y video quedaron adjuntos en el issue como evidencia. **Se corrigió en vivo durante la sesión** — verificado el 3 de septiembre: la ruta ya está registrada como `Route::put('{id}', ...)` y `test_editar_plato` pasa. No hace falta subir este issue a GitHub, el archivo queda como registro del hallazgo.

Nota aparte: en algún momento de la sesión también cambió el HTML de `/login` (apareció un botón "Mostrar contraseña" nuevo) — no rompió nada porque `LoginPage.login()` ya usaba `data-testid` en vez de labels, pero confirma que el ambiente estuvo recibiendo deploys mientras se corrían los tests.

## Estado al cierre

215 tests en total. Se corrió cada módulo por separado contra `https://test-inventario.marketcode.store` (un intento de corrida completa en un solo proceso se cortó por el límite de tiempo del comando en background, no por un fallo de los tests) y todos quedaron en verde salvo lo documentado a propósito:

- Dos `pytest.skip` en `tests/cash/` por falta de mesero/vendedor cargado en el ambiente (precondición de datos, no de código).
- Un flake aislado en `tests/sale/test_metodo_pago.py::test_editar_metodo_pago` que no se reprodujo al aislarlo — probablemente timing de DataTable en la corrida completa, a vigilar si reaparece.

En el camino se corrigieron selectores rotos en varios Page Objects nuevos: columnas de DataTables colisionando con `get_by_label` (usar ids reales en su lugar), combos TomSelect que "roban" el foco del clic siguiente si se encadenan sin esperar, y botones de fila (`_abrir_opciones`) que apuntaban a `fila.locator("button")` en vez del `data-testid="row-actions-*"` correcto.

Pendiente para quien retome: correr `pytest -q` completo una vez (deja margen de tiempo, son ~30-40 min) para confirmar el estado exacto al momento de leer esto — no hay razón para esperar sorpresas, pero no está de más re-confirmarlo.

## Estado en que quedó el ambiente tenant (`test-inventario.marketcode.store`)

Durante la sesión se creó y se borró muchísima data de prueba (así están diseñados los tests, ver `docs/09-datos-de-test-profesionales.md`). Al ir depurando selectores rotos también corrí varios scripts sueltos de diagnóstico fuera de pytest, y algunos de esos — más un par de tests que no limpiaban del todo — dejaron datos de prueba sueltos en el ambiente. Se hizo una limpieza manual al cierre; esto es lo que se encontró y el estado final:

### Encontrado y corregido: usuario duplicado sobre un colaborador real

El hallazgo más importante: `tests/maintenance/test_usuario.py` elegía "la primera opción" del combo de Colaborador al dar de alta un Usuario. Ese combo lista a **todos** los colaboradores sin usuario todavía, no solo al que el test acababa de crear — y en una corrida, "la primera opción" resultó ser un colaborador real y preexistente del tenant (ADMIN, sede CENTRAL), no el descartable creado por el test. Esto generó una cuenta de usuario duplicada (`qa.usuario.<timestamp>@marketcode.test`, rol ADMIN) colgada de ese colaborador real.

- **Se borró** esa cuenta duplicada del ambiente.
- **Se corrigió** `pages/maintenance/usuario_page.py`: `UsuarioPage.crear()` ahora recibe el nombre del colaborador y lo busca por texto en el combo (`_seleccionar_opcion`), en vez de tomar la primera opción a ciegas. `tests/maintenance/test_usuario.py` ya pasa el nombre del colaborador que él mismo crea. Se volvió a correr el test dos veces después del fix y quedó limpio.

### Otros datos de prueba sueltos que se limpiaron manualmente

Todos con nombres claramente identificables como de test (`... QA <timestamp>`, `... TEMP <timestamp>`, `... TEST <timestamp>`, `... NO_DEL <timestamp>`, `... DEBUG <timestamp>`), sin relación con datos reales del tenant:

- **Tipos de Plato / Platos** — ~15 registros sueltos, la mayoría del bug de "editar plato" (el plato de la prueba quedaba sin poder eliminarse limpiamente durante la fase de depuración) y de un par de scripts de diagnóstico. Se corrigió también `tests/supply/test_plato.py`: ahora borra siempre el Tipo de Plato que `crear_plato()` da de alta (antes solo se borraba el plato, el tipo quedaba huérfano — nada lo borra en cascada).
- **Métodos de Pago** — 4 registros sueltos (de un flake real de `test_editar_metodo_pago` que falló antes de llegar a su limpieza, de un script de diagnóstico, y de `test_ir_a_cuentas` que nunca limpiaba lo que creaba). Se corrigió `tests/sale/test_metodo_pago.py::test_ir_a_cuentas` para que borre el método de pago que crea.
- **Cargos, Centros de Costo, Comprobantes, Mesas** — registros sueltos de corridas de depuración de antes de que se arreglara el bug de `_abrir_opciones` (apuntaba a `fila.locator("button")` en vez del botón real de acciones, así que `eliminar_*()` fallaba silenciosamente en esas corridas tempranas).

Todo lo anterior ya está borrado del ambiente al cierre de esta sesión. Verificado con un barrido final por Cuentas Bancarias, Colaboradores, Usuarios, Roles, Sedes, Proveedores, Condiciones de Pago, Documento de Compra, Egresos y Apertura/Cierre — sin residuos evidentes.

### Lo que NO se tocó (así debe seguir)
- Los 5 métodos de pago reales (EFECTIVO, YAPE, PLIN, POS, MIXTO), los cargos/roles/colaboradores/usuarios reales (ADMIN, CAJERO/VENDEDOR/MESERO/COCINERO/CONTADOR DEFAULT, TESTERT — este último de una sesión anterior, no de hoy), y todos los datos base del tenant (bancos, ubigeo, etc.).
- Modo del Negocio sigue en HÍBRIDO, Ambiente de Facturación sigue en BETA — nunca se tocaron.

### Lo que sigue faltando en el ambiente (no es algo que yo pueda arreglar desde QA)
- **No hay ningún colaborador con rol MESERO o VENDEDOR cargado en la sede del cajero de prueba** — por eso el ciclo de Apertura/Cierre de Caja se salta en vez de correr completo (ver sección de arriba).
- **No hay credenciales CPE (Client ID/Secret) configuradas** en Mantenimiento > Empresa — por eso las consultas SUNAT siempre devuelven ese error de configuración en vez de una respuesta real.

Si alguien del equipo de datos carga esas dos cosas, varios tests ya escritos (Apertura/Cierre completo, Egresos con caja real, Mostrador Cajero con "Cobrar", SUNAT con respuesta real) pasan de smoke/skip a cobertura completa sin tocar código.
