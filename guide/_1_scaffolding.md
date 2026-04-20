# 📦 Paso 1 de 4 — `_1_scaffolding`

**Objetivo:** Construir desde cero la estructura completa de un addon de Odoo funcional que gestione actividades de un gimnasio, con entorno de desarrollo ya listo para arrancar.

---

## 🧠 ¿Qué se hizo y por qué tiene sentido aquí?

Este es el punto de partida. Se levanta el entorno (Odoo + base de datos PostgreSQL corriendo con Docker) y se crea el esqueleto mínimo de un módulo Odoo.

En Odoo, un addon es básicamente una carpeta con una estructura de archivos muy concreta que el framework reconoce. Sin ella, Odoo no sabe que el módulo existe. Lo que se hace aquí es exactamente eso: declarar que existe un módulo llamado `gym_addon`, describir qué datos maneja (una tabla `gym_activity`), qué pantallas tiene, y quién puede acceder.

Al terminar este commit, si arrancas el contenedor y activas el módulo, ya tienes una pantalla real en Odoo donde puedes ver y crear "Actividades de gimnasio". Nada de esto requirió escribir HTML, CSS ni consultas SQL a mano — Odoo lo genera todo a partir de tus declaraciones.

---

## 🗁 Vista general de ficheros

```
odoo_intro/
├── 🟢 .gitignore
├── 🟢 docker-compose.yml
└── addons/
    └── gym_addon/
        ├── 🟢 __init__.py
        ├── 🟢 __manifest__.py
        ├── models/
        │   ├── 🟢 __init__.py
        │   └── 🟢 gym_activity.py
        ├── security/
        │   └── 🟢 ir.model.access.csv
        └── views/
            └── 🟢 gym_activity_views.xml
```

🟢 Nuevo &nbsp;&nbsp; 🟡 Modificado &nbsp;&nbsp; 🔴 Eliminado

---

## 🗂️ Archivos afectados

### `docker-compose.yml` — 🟢 NUEVO

```diff
services:
  web:
    image: odoo:17.0
    command: odoo --log-level=debug --country=es
    depends_on:
      - db
    ports:
      - "80:8069"
    volumes:
      - ./addons:/mnt/extra-addons
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
```

> Arranca dos contenedores: uno con Odoo 17 (el servidor web en el puerto 80) y otro con PostgreSQL 15 (la base de datos). La carpeta `./addons` del proyecto se monta directamente en el contenedor, así que cualquier cambio en el código se refleja sin reconstruir la imagen.

---

### `.gitignore` — 🟢 NUEVO

```diff
*/**/__pycache__
```

> Ignora las carpetas `__pycache__` que Python genera automáticamente al compilar. No tiene sentido commitear bytecode generado.

---

### `addons/gym_addon/__manifest__.py` — 🟢 NUEVO

```diff
{
    'name': 'Gym Addon',
    'version': '17.0.1.0.0',
    'summary': 'Gestión de gimnasio',
    'description': 'Módulo para la gestión de actividades y abonados de un gimnasio.',
    'category': 'Services',
    'author': 'Formación Odoo',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_activity_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
```

> Es el `package.json` del addon: le dice a Odoo cómo se llama el módulo, de qué otros módulos depende (`base` es el núcleo mínimo) y qué archivos de datos/vistas debe cargar al instalar. Si este archivo no existe, Odoo no reconoce la carpeta como módulo.

---

### `addons/gym_addon/__init__.py` — 🟢 NUEVO

```diff
from . import models
```

> En Python, para que una carpeta sea un "paquete importable", necesita un `__init__.py`. Este le dice al intérprete: *"cuando alguien importe este paquete, carga también la subcarpeta `models`"*. Equivalente a un `index.js` en Node.

---

### `addons/gym_addon/models/__init__.py` — 🟢 NUEVO

```diff
from . import gym_activity
```

> Mismo patrón: hace que la carpeta `models` sea un paquete Python y carga el archivo `gym_activity.py` al arrancar el addon.

---

### `addons/gym_addon/models/gym_activity.py` — 🟢 NUEVO

```diff
from odoo import models, fields


class GymActivity(models.Model):
    _name = 'gym.activity'
    _description = 'Actividad del gimnasio'

    name = fields.Char(
        string='Nombre',
        required=True,
    )
    description = fields.Text(
        string='Descripción',
    )
    max_capacity = fields.Integer(
        string='Capacidad máxima',
        default=20,
    )
    duration = fields.Float(
        string='Duración (horas)',
        default=1.0,
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )
```

> Aquí está el corazón del commit. Esta clase Python equivale a una tabla en base de datos. Cada `fields.Char`, `fields.Integer`, etc. se convierte en una columna SQL. Odoo genera automáticamente el `CREATE TABLE` correspondiente sin que escribamos SQL. El atributo `_name = 'gym.activity'` es el identificador técnico que usarán las vistas XML para referirse a este modelo.

| Campo Python | Tipo SQL | Equivalente Java |
|---|---|---|
| `fields.Char` | `VARCHAR` | `String` |
| `fields.Text` | `TEXT` | `String` (largo) |
| `fields.Integer` | `INTEGER` | `int` |
| `fields.Float` | `FLOAT` | `double` |
| `fields.Boolean` | `BOOLEAN` | `boolean` |

---

### `addons/gym_addon/security/ir.model.access.csv` — 🟢 NUEVO

```diff
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_gym_activity,access.gym.activity,model_gym_activity,base.group_user,1,1,1,1
```

> Sin este archivo, Odoo bloquea el acceso al modelo aunque exista. Cada fila define una regla de acceso: qué grupo de usuarios tiene permiso de lectura (`perm_read`), escritura, creación y borrado. Aquí se da acceso total (`1,1,1,1`) a todos los usuarios normales (`base.group_user`).

---

### `addons/gym_addon/views/gym_activity_views.xml` — 🟢 NUEVO

```diff
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- Vista lista -->
    <record id="gym_activity_view_tree" model="ir.ui.view">
        <field name="name">gym.activity.tree</field>
        <field name="model">gym.activity</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="duration"/>
                <field name="max_capacity"/>
                <field name="active"/>
            </tree>
        </field>
    </record>

    <!-- Vista formulario -->
    <record id="gym_activity_view_form" model="ir.ui.view">
        <field name="name">gym.activity.form</field>
        <field name="model">gym.activity</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="duration"/>
                        <field name="max_capacity"/>
                        <field name="active"/>
                    </group>
                    <group string="Descripción">
                        <field name="description" nolabel="1" colspan="2"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Acción de ventana -->
    <record id="gym_activity_action" model="ir.actions.act_window">
        <field name="name">Actividades</field>
        <field name="res_model">gym.activity</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Menús -->
    <menuitem id="gym_menu_root"
              name="Gimnasio"
              sequence="10"/>

    <menuitem id="gym_menu_activities"
              name="Actividades"
              parent="gym_menu_root"
              action="gym_activity_action"
              sequence="10"/>
 
</odoo>
```

> El XML de vistas es donde más se nota la filosofía de Odoo: describes *qué quieres mostrar*, no *cómo dibujarlo*. Hay tres piezas:
> - **Vista árbol** (`<tree>`): la tabla/listado con columnas
> - **Vista formulario** (`<form>`): el detalle de un registro, con grupos que forman filas de campos
> - **Acción + Menús**: crean la entrada "Gimnasio > Actividades" en la barra de navegación de Odoo
>
> Si conoces HTML, piensa en esto como si escribieras solo el `<form>` con los `<input>` etiquetados, y Odoo se encargase automáticamente del CSS, la validación, los botones de guardar/cancelar, la paginación y la conexión a la base de datos.

---

✅ **Resultado final de este paso:** un módulo instalable que crea una tabla `gym_activity` en PostgreSQL y muestra en Odoo una pantalla funcional para gestionar actividades de gimnasio.
