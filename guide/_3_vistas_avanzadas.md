# 🎨 Paso 3 de 4 — `_3_vistas_avanzadas`

**Objetivo:** Añadir vistas Kanban a los dos modelos existentes, introduciendo una forma visual de presentar la información y el concepto de plantillas con lógica en las vistas XML de Odoo.

---

## 🧠 ¿Qué se hizo y por qué tiene sentido aquí?

Hasta ahora las pantallas eran siempre lo mismo: una tabla de filas y un formulario de detalle. En este paso se introduce un tercer tipo de vista: el **Kanban** — esas tarjetas visuales organizadas en columnas que conoces de herramientas como Trello.

Lo interesante es que en Odoo el Kanban no es solo estético. Cuando se usa con `default_group_by`, agrupa automáticamente los registros por un campo: en este caso los horarios se agrupan por `day_of_week`, creando una columna por cada día de la semana. Es una vista de calendario semanal hecha con unas pocas líneas de XML.

Además, la vista Kanban introduce algo nuevo en la sintaxis: **plantillas con `<t t-name>`**, que son fragmentos de HTML reutilizables con variables. Si conoces los *templates* de JavaScript (Handlebars, Vue, Angular), es exactamente el mismo concepto.

---

## 🗁 Vista general de ficheros

```
addons/gym_addon/
├── 🟡 __manifest__.py
└── views/
    ├── 🟡 gym_activity_views.xml
    └── 🟡 gym_schedule_views.xml
```

🟢 Nuevo &nbsp;&nbsp; 🟡 Modificado &nbsp;&nbsp; 🔴 Eliminado

---

## 🗂️ Archivos afectados

### `addons/gym_addon/views/gym_activity_views.xml` — 🟡 MODIFICADO

**Bloque 1 — Nueva vista Kanban de actividades:**

```diff
  14      </record>
  15 
  16 +     <!-- Vista Kanban de actividades -->
  17 +     <record id="gym_activity_view_kanban" model="ir.ui.view">
  18 +         <field name="name">gym.activity.kanban</field>
  19 +         <field name="model">gym.activity</field>
  20 +         <field name="arch" type="xml">
  21 +             <kanban>
  22 +                 <field name="name"/>
  23 +                 <field name="duration"/>
  24 +                 <field name="max_capacity"/>
  25 +                 <templates>
  26 +                     <t t-name="kanban-box">
  27 +                         <div class="oe_kanban_card oe_kanban_global_click">
  28 +                             <div class="oe_kanban_content">
  29 +                                 <strong>
  30 +                                     <field name="name"/>
  31 +                                 </strong>
  32 +                                 <div class="text-muted">
  33 +                                     <field name="duration"/> h · max
  34 +                                     <field name="max_capacity"/> personas
  35 +                                 </div>
  36 +                             </div>
  37 +                         </div>
  38 +                     </t>
  39 +                 </templates>
  40 +             </kanban>
  41 +         </field>
  42 +     </record>
```

> Dentro del `<kanban>` primero se declaran los campos que se van a usar (para que Odoo los cargue), y luego viene la plantilla `<t t-name="kanban-box">` que define el HTML de cada tarjeta. Las clases CSS como `oe_kanban_card` son del framework de Odoo y dan el estilo de tarjeta. `oe_kanban_global_click` hace que clicar en cualquier parte de la tarjeta abra el formulario del registro.

**Bloque 2 — Acción ampliada con kanban:**

```diff
  74      <record id="gym_activity_action" model="ir.actions.act_window">
  75          <field name="name">Actividades</field>
  76          <field name="res_model">gym.activity</field>
  77 -        <field name="view_mode">tree,form</field>
  78 +        <field name="view_mode">kanban,tree,form</field>
  79      </record>
```

> El orden importa: el primer modo en la lista es el que se muestra por defecto al entrar en la pantalla. Al poner `kanban` primero, los usuarios verán las tarjetas al abrir "Actividades" en lugar de la tabla.

---

### `addons/gym_addon/views/gym_schedule_views.xml` — 🟡 MODIFICADO

**Bloque 1 — Nueva vista Kanban de horarios agrupada por día:**

```diff
  15      </record>
  16 
  17 +     <!-- Kanban del horario agrupado por día -->
  18 +     <record id="gym_schedule_view_kanban" model="ir.ui.view">
  19 +         <field name="name">gym.schedule.kanban</field>
  20 +         <field name="model">gym.schedule</field>
  21 +         <field name="arch" type="xml">
  22 +             <kanban default_group_by="day_of_week">
  23 +                 <field name="activity_id"/>
  24 +                 <field name="time_start"/>
  25 +                 <field name="time_end"/>
  26 +                 <field name="instructor"/>
  27 +                 <templates>
  28 +                     <t t-name="kanban-box">
  29 +                         <div class="oe_kanban_card oe_kanban_global_click">
  30 +                             <strong>
  31 +                                 <field name="activity_id"/>
  32 +                             </strong>
  33 +                             <div class="text-muted">
  34 +                                 <field name="time_start" widget="float_time"/> -
  35 +                                 <field name="time_end" widget="float_time"/>
  36 +                             </div>
  37 +                             <div>
  38 +                                 <field name="instructor"/>
  39 +                             </div>
  40 +                         </div>
  41 +                     </t>
  42 +                 </templates>
  43 +             </kanban>
  44 +         </field>
  45 +     </record>
```

> La clave aquí es `default_group_by="day_of_week"`: Odoo crea automáticamente una columna por cada valor del campo `Selection` (Lunes, Martes…) y coloca cada horario en su columna correspondiente. El resultado visual es una vista de semana — sin una sola línea de JavaScript.

**Bloque 2 — Acción ampliada con kanban:**

```diff
  66      <record id="gym_schedule_action" model="ir.actions.act_window">
  67          <field name="name">Horario semanal</field>
  68          <field name="res_model">gym.schedule</field>
  69 -        <field name="view_mode">tree,form</field>
  70 +        <field name="view_mode">kanban,tree,form</field>
  71      </record>
```

---

### `addons/gym_addon/__manifest__.py` — 🟡 MODIFICADO

```diff
  2 -    'version': '17.0.2.0.0',
  3 +    'version': '17.0.3.0.0',
```

> Bump de versión para que Odoo detecte que hay cambios al actualizar el módulo.

---

✅ **Resultado final de este paso:** las pantallas de Actividades y Horario semanal ahora tienen vista Kanban como vista por defecto. El horario aparece organizado en columnas por día de la semana, como un tablero semanal, sin haber escrito JavaScript ni CSS propio.
