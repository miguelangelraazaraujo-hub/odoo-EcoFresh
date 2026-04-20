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
>    </record>
>
     <!-- Vista Kanban de actividades -->
     <record id="gym_activity_view_kanban" model="ir.ui.view">
         <field name="name">gym.activity.kanban</field>
         <field name="model">gym.activity</field>
         <field name="arch" type="xml">
             <kanban>
                 <field name="name"/>
                 <field name="duration"/>
                 <field name="max_capacity"/>
                 <templates>
                     <t t-name="kanban-box">
                         <div class="oe_kanban_card oe_kanban_global_click">
                             <div class="oe_kanban_content">
                                 <strong>
                                     <field name="name"/>
                                 </strong>
                                 <div class="text-muted">
                                     <field name="duration"/> h · max
                                     <field name="max_capacity"/> personas
                                 </div>
                             </div>
                         </div>
                     </t>
                 </templates>
             </kanban>
         </field>
     </record>
```

> Dentro del `<kanban>` primero se declaran los campos que se van a usar (para que Odoo los cargue), y luego viene la plantilla `<t t-name="kanban-box">` que define el HTML de cada tarjeta. Las clases CSS como `oe_kanban_card` son del framework de Odoo y dan el estilo de tarjeta. `oe_kanban_global_click` hace que clicar en cualquier parte de la tarjeta abra el formulario del registro.

**Bloque 2 — Acción ampliada con kanban:**

```diff
>   <record id="gym_activity_action" model="ir.actions.act_window">
>       <field name="name">Actividades</field>
>       <field name="res_model">gym.activity</field>
        <field name="view_mode">kanban,tree,form</field>
>   </record>
```

> El orden importa: el primer modo en la lista es el que se muestra por defecto al entrar en la pantalla. Al poner `kanban` primero, los usuarios verán las tarjetas al abrir "Actividades" en lugar de la tabla.

---

### `addons/gym_addon/views/gym_schedule_views.xml` — 🟡 MODIFICADO

**Bloque 1 — Nueva vista Kanban de horarios agrupada por día:**

```diff
>    </record>
>
     <!-- Kanban del horario agrupado por día -->
     <record id="gym_schedule_view_kanban" model="ir.ui.view">
         <field name="name">gym.schedule.kanban</field>
         <field name="model">gym.schedule</field>
         <field name="arch" type="xml">
             <kanban default_group_by="day_of_week">
                 <field name="activity_id"/>
                 <field name="time_start"/>
                 <field name="time_end"/>
                 <field name="instructor"/>
                 <templates>
                     <t t-name="kanban-box">
                         <div class="oe_kanban_card oe_kanban_global_click">
                             <strong>
                                 <field name="activity_id"/>
                             </strong>
                             <div class="text-muted">
                                 <field name="time_start" widget="float_time"/> -
                                 <field name="time_end" widget="float_time"/>
                             </div>
                             <div>
                                 <field name="instructor"/>
                             </div>
                         </div>
                     </t>
                 </templates>
             </kanban>
         </field>
     </record>
```

> La clave aquí es `default_group_by="day_of_week"`: Odoo crea automáticamente una columna por cada valor del campo `Selection` (Lunes, Martes…) y coloca cada horario en su columna correspondiente. El resultado visual es una vista de semana — sin una sola línea de JavaScript.

**Bloque 2 — Acción ampliada con kanban:**

```diff
>   <record id="gym_schedule_action" model="ir.actions.act_window">
>       <field name="name">Horario semanal</field>
>       <field name="res_model">gym.schedule</field>
        <field name="view_mode">kanban,tree,form</field>
>   </record>
```

---

### `addons/gym_addon/__manifest__.py` — 🟡 MODIFICADO

```diff
    'version': '17.0.3.0.0',
```

> Bump de versión para que Odoo detecte que hay cambios al actualizar el módulo.

---

✅ **Resultado final de este paso:** las pantallas de Actividades y Horario semanal ahora tienen vista Kanban como vista por defecto. El horario aparece organizado en columnas por día de la semana, como un tablero semanal, sin haber escrito JavaScript ni CSS propio.
