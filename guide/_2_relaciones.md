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
from odoo import models, fields


class GymSchedule(models.Model):
    _name = 'gym.schedule'
    _description = 'Horario semanal de actividades'
    _order = 'day_of_week, time_start'

    # Many2one → cada horario pertenece a UNA actividad
    activity_id = fields.Many2one(
        comodel_name='gym.activity',
        string='Actividad',
        required=True,
        ondelete='cascade',
    )
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Lunes'),
            ('1', 'Martes'),
            ('2', 'Miércoles'),
            ('3', 'Jueves'),
            ('4', 'Viernes'),
            ('5', 'Sábado'),
            ('6', 'Domingo'),
        ],
        string='Día de la semana',
        required=True,
    )
    time_start = fields.Float(string='Hora de inicio', required=True)
    time_end   = fields.Float(string='Hora de fin',    required=True)
    instructor = fields.Char(string='Monitor/a')
```

> `_order = 'day_of_week, time_start'` hace que los registros se ordenen automáticamente por día y hora, igual que un `ORDER BY` en SQL. El `ondelete='cascade'` significa que si se borra una actividad, sus horarios se borran en cascada (como `ON DELETE CASCADE` en SQL). `fields.Selection` es el equivalente a un `ENUM`: una lista cerrada de opciones válidas.

---

### `addons/gym_addon/models/gym_activity.py` — 🟡 MODIFICADO

```diff
>   active = fields.Boolean(
>      string='Activo',
>       default=True,
>   )

     # Relación inversa: desde la actividad vemos todos sus horarios
     schedule_ids = fields.One2many(
         comodel_name='gym.schedule',
         inverse_name='activity_id',
         string='Horarios',
     )
```

> Este campo **no crea ninguna columna nueva** en la tabla `gym_activity`. Es puramente una declaración que le dice a Odoo: *"cuando alguien pida los horarios de esta actividad, busca en `gym_schedule` todos los registros donde `activity_id` apunte a mí"*. Es exactamente lo que haría un `SELECT * FROM gym_schedule WHERE activity_id = ?` en SQL. La convención `_ids` (plural) indica que devuelve una colección.

---

### `addons/gym_addon/models/__init__.py` — 🟡 MODIFICADO

```diff
from . import gym_activity
from . import gym_schedule
```

> Se registra el nuevo modelo para que Python lo cargue al arrancar.

---

### `addons/gym_addon/views/gym_schedule_views.xml` — 🟢 NUEVO

```diff
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="gym_schedule_view_tree" model="ir.ui.view">
        <field name="model">gym.schedule</field>
        <field name="arch" type="xml">
            <tree>
                <field name="day_of_week"/>
                <field name="activity_id"/>
                <field name="time_start" widget="float_time"/>
                <field name="time_end"   widget="float_time"/>
                <field name="instructor"/>
            </tree>
        </field>
    </record>

    <record id="gym_schedule_view_form" model="ir.ui.view">
       <field name="model">gym.schedule</field>
       <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="activity_id"/>
                        <field name="day_of_week"/>
                        <field name="time_start" widget="float_time"/>
                        <field name="time_end"   widget="float_time"/>
                        <field name="instructor"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
    <record id="gym_schedule_action" model="ir.actions.act_window">
        <field name="name">Horario semanal</field>
         <field name="res_model">gym.schedule</field>
        <field name="view_mode">tree,form</field>
    </record>

    <menuitem id="gym_menu_schedule"
              name="Horario semanal"
              parent="gym_menu_root"
              action="gym_schedule_action"
              sequence="20"/>

</odoo>
```

> Mismo patrón que las vistas de actividad, pero con un detalle nuevo: `widget="float_time"`. Los campos de hora se guardan como `Float` (9.5 = 9:30h), pero el widget `float_time` los presenta al usuario como `09:30` en lugar de `9.5`. Es la separación entre *cómo se almacena* y *cómo se muestra*.

---

### `addons/gym_addon/views/gym_activity_views.xml` — 🟡 MODIFICADO

```diff
>       <group string="Descripción">
>           <field name="description" nolabel="1" colspan="2"/>
>       </group>
        <!-- Lista de horarios embebida en la ficha de actividad -->
         <notebook>
             <page string="Horarios">
                 <field name="schedule_ids">
                     <tree editable="bottom">
                         <field name="day_of_week"/>
                         <field name="time_start" widget="float_time"/>
                         <field name="time_end"   widget="float_time"/>
                         <field name="instructor"/>
                     </tree>
                 </field>
             </page>
         </notebook>
         </sheet>
```

> `<notebook>` genera pestañas dentro del formulario. `editable="bottom"` permite editar la tabla de horarios directamente en la línea, sin abrir un popup, añadiendo filas nuevas al final. Es el patrón "master-detail" clásico: ficha principal (actividad) con tabla de detalle (horarios) integrada.

---

### `addons/gym_addon/security/ir.model.access.csv` — 🟡 MODIFICADO

```diff
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_gym_activity,access.gym.activity,model_gym_activity,base.group_user,1,1,1,1
access_gym_schedule,access.gym.schedule,model_gym_schedule,base.group_user,1,1,1,1
```

> Cada nuevo modelo necesita su propia fila de permisos. Si se olvida, Odoo lanza un error de acceso al intentar mostrar los horarios.

---

### `addons/gym_addon/__manifest__.py` — 🟡 MODIFICADO

```diff
>   'data': [
>       'security/ir.model.access.csv',
>       'views/gym_activity_views.xml',
        'views/gym_schedule_views.xml',
>   ],
    'version': '17.0.2.0.0',
```

> Se registra el nuevo archivo de vistas y se sube la versión del módulo. En Odoo, cambiar la versión en el manifest le indica al sistema que debe ejecutar una actualización del módulo para aplicar los cambios de estructura en la base de datos.

---

✅ **Resultado final de este paso:** el módulo ahora gestiona dos tablas relacionadas. Desde la ficha de una actividad se pueden añadir sus horarios semanales directamente en una pestaña embebida, y también existe una vista global "Horario semanal" en el menú.
