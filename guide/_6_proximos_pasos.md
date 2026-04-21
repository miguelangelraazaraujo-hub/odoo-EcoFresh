## PROPUESTA PARA LOS PRÓXIMOS PASOS

Ampliar el proyecto introduciendo los abonados que esten relacionados con res.partner y los productos como suscripciones para la gestión de cobros.
Incluso crear una pequeña gestión de caja de ejectivo y cobro mensual.

---

**Paso 6 — `_6_herencia_partner`**

El concepto estrella es la **herencia de modelos**. En lugar de crear un modelo `gym.member` desde cero, se extiende `res.partner` añadiéndole campos propios del gimnasio: número de abonado, fecha de alta, tipo de abono. Los alumnos ven por primera vez `_inherit` en lugar de `_name`, y entienden que están modificando una tabla existente de Odoo sin tocar su código fuente. Es el equivalente a la herencia de clases en Java pero aplicado a la base de datos.

---

**Paso 7 — `_7_productos_abono`**

Aquí se introduce la relación con `product.template` para crear los tipos de abono (mensual, trimestral, anual) como productos de Odoo. El concepto clave es aprender a relacionar tu modelo con modelos de otros módulos de Odoo — no solo con los tuyos propios. También se introduce el campo `Many2one` apuntando a un modelo heredado, y se añade la dependencia del módulo `product` en el manifest. El resultado visible es que desde la ficha del abonado puedes seleccionar qué tipo de abono tiene contratado.

---

**Paso 8 — `_8_metodos_python`**

Hasta ahora el Python del proyecto es casi solo declaración de campos. En este paso se escribe lógica de negocio real: métodos en el modelo que calculan la fecha de vencimiento del abono, un campo computado (`fields.Date` calculado con `@api.depends`) que muestra si el abono está vigente o vencido, y quizás una acción que renueva el abono. Los alumnos ven la diferencia entre datos declarativos y lógica imperativa dentro del ORM de Odoo. Es el paso más "Python puro" de todos.

---

**Paso 9 — `_9_facturacion`**

El salto a la contabilidad. Se crea una acción que genera una factura (`account.move`) para un abonado a partir de su producto de abono. Los alumnos ven cómo interactuar con módulos complejos de Odoo creando registros en sus modelos desde código propio. El concepto nuevo es el **wizard** (un modelo transitorio con `_transient = True`) que actúa como un formulario de confirmación antes de generar la factura — patrón muy habitual en Odoo para acciones que afectan a múltiples registros.

---

**Paso 10 — `_10_caja_efectivo`**

El paso más avanzado y el más vistoso. Se crea un modelo `gym.cash.session` para registrar aperturas y cierres de caja, con los cobros en efectivo del día. Introduce el concepto de **flujo de estados** con `fields.Selection` y transiciones entre estados (abierta → cerrada), botones en el formulario que ejecutan métodos (`<button type="object">`), y un campo computado que suma el total de la sesión. Si da tiempo, se puede añadir una vista de informe en el portal público con el resumen diario.

---

En total quedaría un proyecto de **10 commits** con una progresión muy clara: declarar → relacionar → visualizar → publicar → heredar → productos → lógica → facturar → caja. Cada paso es autocontenido y los alumnos pueden parar en cualquier punto y tener algo funcional.
