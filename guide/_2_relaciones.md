# 🔗 Paso 2 de 4 — `_2_relaciones`

**Objetivo:** Introducir un segundo modelo (`GymSchedule`) vinculado al primero mediante una relación de base de datos, y aprender cómo Odoo gestiona estas relaciones entre tablas sin escribir JOINs a mano.

---

## 🧠 ¿Qué se hizo y por qué tiene sentido aquí?

Hasta ahora solo existía la tabla de actividades (Yoga, Spinning…). Pero una actividad tiene horarios: se imparte los lunes a las 9h, los miércoles a las 18h, etc. Eso es una relación clásica de base de datos: **una actividad tiene muchos horarios** (`1:N`).

En SQL lo modelarías con una clave foránea (`FOREIGN KEY activity_id REFERENCES gym_activity(id)`). En Odoo se hace con dos campos de relación complementarios:

- `Many2one` en `GymSchedule` → *"este horario pertenece a una actividad"*
- `One2many` en `GymActivity` → *"esta actividad tiene muchos horarios"* (es la vista inversa, no crea columna en BD)

Lo más interesante del paso es la vista embebida: en el formulario de una actividad aparece una pestaña "Horarios" con una tabla editable inline. El usuario puede añadir horarios directamente desde la ficha de la actividad, sin salir a otra pantalla. Odoo gestiona automáticamente el guardado en cascada.

---

## 🗗️ Diagrama de relación

```
gym_activity (1) ──────────── (N) gym_schedule
     id  ◄──────────── activity_id (FK)
     name                day_of_week
     duration            time_start
     ...                 time_end
                         instructor
```

---

## 🗁 Vista general de ficheros

```
addons/gym_addon/
├── 🟡 __manifest__.py
├── models/
│   ├── 🟡 __init__.py
│   ├── 🟡 gym_activity.py
│   └── 🟢 gym_schedule.py
├── security/
│   └── 🟡 ir.model.access.csv
└── views/
    ├── 🟡 gym_activity_views.xml
    └── 🟢 gym_schedule_views.xml
```

🟢 Nuevo &nbsp;&nbsp; 🟡 Modificado &nbsp;&nbsp; 🔴 Eliminado

---

## 🗂️ Archivos afectados

### `addons/gym_addon/models/gym_schedule.py` — 🟢 NUEVO

```diff
  1 + from odoo import models, fields
  2 + 
  3 + 
  4 + class GymSchedule(models.Model):
  5 +     _name = 'gym.schedule'
  6 +     _description = 'Horario semanal de actividades'
  7 +     _order = 'day_of_week, time_start'
  8 + 
  9 +     # Many2one → cada horario pertenece a UNA actividad
 10 +     activity_id = fields.Many2one(
 11 +         comodel_name='gym.activity',
 12 +         string='Actividad',
 13 +         required=True,
 14 +         ondelete='cascade',
 15 +     )
 16 +     day_of_week = fields.Selection(
 17 +         selection=[
 18 +             ('0', 'Lunes'),
 19 +             ('1', 'Martes'),
 20 +             ('2', 'Miércoles'),
 21 +             ('3', 'Jueves'),
 22 +             ('4', 'Viernes'),
 23 +             ('5', 'Sábado'),
 24 +             ('6', 'Domingo'),
 25 +         ],
 26 +         string='Día de la semana',
 27 +         required=True,
 28 +     )
 29 +     time_start = fields.Float(string='Hora de inicio', required=True)
 30 +     time_end   = fields.Float(string='Hora de fin',    required=True)
 31 +     instructor = fields.Char(string='Monitor/a')
```

> `_order = 'day_of_week, time_start'` hace que los registros se ordenen automáticamente por día y hora, igual que un `ORDER BY` en SQL. El `ondelete='cascade'` significa que si se borra una actividad, sus horarios se borran en cascada (como `ON DELETE CASCADE` en SQL). `fields.Selection` es el equivalente a un `ENUM`: una lista cerrada de opciones válidas.

---

### `addons/gym_addon/models/gym_activity.py` — 🟡 MODIFICADO

```diff
  22      active = fields.Boolean(
  23          string='Activo',
  24          default=True,
  25      )
  26 +
  27 +     # Relación inversa: desde la actividad vemos todos sus horarios
  28 +     schedule_ids = fields.One2many(
  29 +         comodel_name='gym.schedule',
  30 +         inverse_name='activity_id',
  31 +         string='Horarios',
  32 +     )
```

> Este campo **no crea ninguna columna nueva** en la tabla `gym_activity`. Es puramente una declaración que le dice a Odoo: *"cuando alguien pida los horarios de esta actividad, busca en `gym_schedule` todos los registros donde `activity_id` apunte a mí"*. Es exactamente lo que haría un `SELECT * FROM gym_schedule WHERE activity_id = ?` en SQL. La convención `_ids` (plural) indica que devuelve una colección.

---

### `addons/gym_addon/models/__init__.py` — 🟡 MODIFICADO

```diff
  1   from . import gym_activity
  2 + from . import gym_schedule
```

> Se registra el nuevo modelo para que Python lo cargue al arrancar.

---

### `addons/gym_addon/views/gym_schedule_views.xml` — 🟢 NUEVO

```diff
  1 + <?xml version="1.0" encoding="utf-8"?>
  2 + <odoo>
  3 + 
  4 +     <record id="gym_schedule_view_tree" model="ir.ui.view">
  5 +         <field name="model">gym.schedule</field>
  6 +         <field name="arch" type="xml">
  7 +             <tree>
  8 +                 <field name="day_of_week"/>
  9 +                 <field name="activity_id"/>
 10 +                 <field name="time_start" widget="float_time"/>
 11 +                 <field name="time_end"   widget="float_time"/>
 12 +                 <field name="instructor"/>
 13 +             </tree>
 14 +         </field>
 15 +     </record>
 16 + 
 17 +     <record id="gym_schedule_view_form" model="ir.ui.view">
 18 +         <field name="model">gym.schedule</field>
 19 +         <field name="arch" type="xml">
 20 +             <form>
 21 +                 <sheet>
 22 +                     <group>
 23 +                         <field name="activity_id"/>
 24 +                         <field name="day_of_week"/>
 25 +                         <field name="time_start" widget="float_time"/>
 26 +                         <field name="time_end"   widget="float_time"/>
 27 +                         <field name="instructor"/>
 28 +                     </group>
 29 +                 </sheet>
 30 +             </form>
 31 +         </field>
 32 +     </record>
 33 + 
 34 +     <record id="gym_schedule_action" model="ir.actions.act_window">
 35 +         <field name="name">Horario semanal</field>
 36 +         <field name="res_model">gym.schedule</field>
 37 +         <field name="view_mode">tree,form</field>
 38 +     </record>
 39 + 
 40 +     <menuitem id="gym_menu_schedule"
 41 +               name="Horario semanal"
 42 +               parent="gym_menu_root"
 43 +               action="gym_schedule_action"
 44 +               sequence="20"/>
 45 + 
 46 + </odoo>
```

> Mismo patrón que las vistas de actividad, pero con un detalle nuevo: `widget="float_time"`. Los campos de hora se guardan como `Float` (9.5 = 9:30h), pero el widget `float_time` los presenta al usuario como `09:30` en lugar de `9.5`. Es la separación entre *cómo se almacena* y *cómo se muestra*.

---

### `addons/gym_addon/views/gym_activity_views.xml` — 🟡 MODIFICADO

```diff
  28          <group string="Descripción">
  29              <field name="description" nolabel="1" colspan="2"/>
  30          </group>
  31 +         <!-- Lista de horarios embebida en la ficha de actividad -->
  32 +         <notebook>
  33 +             <page string="Horarios">
  34 +                 <field name="schedule_ids">
  35 +                     <tree editable="bottom">
  36 +                         <field name="day_of_week"/>
  37 +                         <field name="time_start" widget="float_time"/>
  38 +                         <field name="time_end"   widget="float_time"/>
  39 +                         <field name="instructor"/>
  40 +                     </tree>
  41 +                 </field>
  42 +             </page>
  43 +         </notebook>
  44          </sheet>
```

> `<notebook>` genera pestañas dentro del formulario. `editable="bottom"` permite editar la tabla de horarios directamente en la línea, sin abrir un popup, añadiendo filas nuevas al final. Es el patrón "master-detail" clásico: ficha principal (actividad) con tabla de detalle (horarios) integrada.

---

### `addons/gym_addon/security/ir.model.access.csv` — 🟡 MODIFICADO

```diff
  1   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  2   access_gym_activity,access.gym.activity,model_gym_activity,base.group_user,1,1,1,1
  3 + access_gym_schedule,access.gym.schedule,model_gym_schedule,base.group_user,1,1,1,1
```

> Cada nuevo modelo necesita su propia fila de permisos. Si se olvida, Odoo lanza un error de acceso al intentar mostrar los horarios.

---

### `addons/gym_addon/__manifest__.py` — 🟡 MODIFICADO

```diff
  3      'data': [
  4          'security/ir.model.access.csv',
  5          'views/gym_activity_views.xml',
  6 +        'views/gym_schedule_views.xml',
  7      ],
  8 -    'version': '17.0.1.0.0',
  9 +    'version': '17.0.2.0.0',
```

> Se registra el nuevo archivo de vistas y se sube la versión del módulo. En Odoo, cambiar la versión en el manifest le indica al sistema que debe ejecutar una actualización del módulo para aplicar los cambios de estructura en la base de datos.

---

✅ **Resultado final de este paso:** el módulo ahora gestiona dos tablas relacionadas. Desde la ficha de una actividad se pueden añadir sus horarios semanales directamente en una pestaña embebida, y también existe una vista global "Horario semanal" en el menú.
