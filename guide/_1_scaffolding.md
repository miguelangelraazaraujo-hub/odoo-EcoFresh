# 📦 Paso 1 de 4 — `_1_scaffolding`

**Objetivo:** Construir desde cero la estructura completa de un addon de Odoo funcional que gestione actividades de un gimnasio, con entorno de desarrollo ya listo para arrancar.

---

## 🧠 ¿Qué se hizo y por qué tiene sentido aquí?

Este es el punto de partida. Se levanta el entorno (Odoo + base de datos PostgreSQL corriendo con Docker) y se crea el esqueleto mínimo de un módulo Odoo.

En Odoo, un addon es básicamente una carpeta con una estructura de archivos muy concreta que el framework reconoce. Sin ella, Odoo no sabe que el módulo existe. Lo que se hace aquí es exactamente eso: declarar que existe un módulo llamado `gym_addon`, describir qué datos maneja (una tabla `gym_activity`), qué pantallas tiene, y quién puede acceder.

Al terminar este commit, si arrancas el contenedor y activas el módulo, ya tienes una pantalla real en Odoo donde puedes ver y crear "Actividades de gimnasio". Nada de esto requirió escribir HTML, CSS ni consultas SQL a mano — Odoo lo genera todo a partir de tus declaraciones.

---

## 🗂️ Archivos afectados

### `docker-compose.yml` — 🟢 NUEVO

```diff
  1 + services:
  2 +   web:
  3 +     image: odoo:17.0
  4 +     command: odoo --log-level=debug --country=es
  5 +     depends_on:
  6 +       - db
  7 +     ports:
  8 +       - "80:8069"
  9 +     volumes:
 10 +       - ./addons:/mnt/extra-addons
 11 +     environment:
 12 +       - HOST=db
 13 +       - USER=odoo
 14 +       - PASSWORD=odoo
 15 + 
 16 +   db:
 17 +     image: postgres:15
 18 +     environment:
 19 +       - POSTGRES_DB=postgres
 20 +       - POSTGRES_PASSWORD=odoo
 21 +       - POSTGRES_USER=odoo
```

> Arranca dos contenedores: uno con Odoo 17 (el servidor web en el puerto 80) y otro con PostgreSQL 15 (la base de datos). La carpeta `./addons` del proyecto se monta directamente en el contenedor, así que cualquier cambio en el código se refleja sin reconstruir la imagen.

---

### `.gitignore` — 🟢 NUEVO

```diff
  1 + */**/__pycache__
```

> Ignora las carpetas `__pycache__` que Python genera automáticamente al compilar. No tiene sentido commitear bytecode generado.

---

### `addons/gym_addon/__manifest__.py` — 🟢 NUEVO

```diff
  1 + {
  2 +     'name': 'Gym Addon',
  3 +     'version': '17.0.1.0.0',
  4 +     'summary': 'Gestión de gimnasio',
  5 +     'description': 'Módulo para la gestión de actividades y abonados de un gimnasio.',
  6 +     'category': 'Services',
  7 +     'author': 'Formación Odoo',
  8 +     'depends': ['base'],
  9 +     'data': [
 10 +         'security/ir.model.access.csv',
 11 +         'views/gym_activity_views.xml',
 12 +     ],
 13 +     'installable': True,
 14 +     'application': True,
 15 +     'license': 'LGPL-3',
 16 + }
```

> Es el `package.json` del addon: le dice a Odoo cómo se llama el módulo, de qué otros módulos depende (`base` es el núcleo mínimo) y qué archivos de datos/vistas debe cargar al instalar. Si este archivo no existe, Odoo no reconoce la carpeta como módulo.

---

### `addons/gym_addon/__init__.py` — 🟢 NUEVO

```diff
  1 + from . import models
```

> En Python, para que una carpeta sea un "paquete importable", necesita un `__init__.py`. Este le dice al intérprete: *"cuando alguien importe este paquete, carga también la subcarpeta `models`"*. Equivalente a un `index.js` en Node.

---

### `addons/gym_addon/models/__init__.py` — 🟢 NUEVO

```diff
  1 + from . import gym_activity
```

> Mismo patrón: hace que la carpeta `models` sea un paquete Python y carga el archivo `gym_activity.py` al arrancar el addon.

---

### `addons/gym_addon/models/gym_activity.py` — 🟢 NUEVO

```diff
  1 + from odoo import models, fields
  2 + 
  3 + 
  4 + class GymActivity(models.Model):
  5 +     _name = 'gym.activity'
  6 +     _description = 'Actividad del gimnasio'
  7 + 
  8 +     name = fields.Char(
  9 +         string='Nombre',
  10 +         required=True,
  11 +     )
  12 +     description = fields.Text(
  13 +         string='Descripción',
  14 +     )
  15 +     max_capacity = fields.Integer(
  16 +         string='Capacidad máxima',
  17 +         default=20,
  18 +     )
  19 +     duration = fields.Float(
  20 +         string='Duración (horas)',
  21 +         default=1.0,
  22 +     )
  23 +     active = fields.Boolean(
  24 +         string='Activo',
  25 +         default=True,
  26 +     )
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
  1 + id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
  2 + access_gym_activity,access.gym.activity,model_gym_activity,base.group_user,1,1,1,1
```

> Sin este archivo, Odoo bloquea el acceso al modelo aunque exista. Cada fila define una regla de acceso: qué grupo de usuarios tiene permiso de lectura (`perm_read`), escritura, creación y borrado. Aquí se da acceso total (`1,1,1,1`) a todos los usuarios normales (`base.group_user`).

---

### `addons/gym_addon/views/gym_activity_views.xml` — 🟢 NUEVO

```diff
  1 + <?xml version="1.0" encoding="utf-8"?>
  2 + <odoo>
  3 + 
  4 +     <!-- Vista lista -->
  5 +     <record id="gym_activity_view_tree" model="ir.ui.view">
  6 +         <field name="name">gym.activity.tree</field>
  7 +         <field name="model">gym.activity</field>
  8 +         <field name="arch" type="xml">
  9 +             <tree>
 10 +                 <field name="name"/>
 11 +                 <field name="duration"/>
 12 +                 <field name="max_capacity"/>
 13 +                 <field name="active"/>
 14 +             </tree>
 15 +         </field>
 16 +     </record>
 17 + 
 18 +     <!-- Vista formulario -->
 19 +     <record id="gym_activity_view_form" model="ir.ui.view">
 20 +         <field name="name">gym.activity.form</field>
 21 +         <field name="model">gym.activity</field>
 22 +         <field name="arch" type="xml">
 23 +             <form>
 24 +                 <sheet>
 25 +                     <group>
 26 +                         <field name="name"/>
 27 +                         <field name="duration"/>
 28 +                         <field name="max_capacity"/>
 29 +                         <field name="active"/>
 30 +                     </group>
 31 +                     <group string="Descripción">
 32 +                         <field name="description" nolabel="1" colspan="2"/>
 33 +                     </group>
 34 +                 </sheet>
 35 +             </form>
 36 +         </field>
 37 +     </record>
 38 + 
 39 +     <!-- Acción de ventana -->
 40 +     <record id="gym_activity_action" model="ir.actions.act_window">
 41 +         <field name="name">Actividades</field>
 42 +         <field name="res_model">gym.activity</field>
 43 +         <field name="view_mode">tree,form</field>
 44 +     </record>
 45 + 
 46 +     <!-- Menús -->
 47 +     <menuitem id="gym_menu_root"
 48 +               name="Gimnasio"
 49 +               sequence="10"/>
 50 + 
 51 +     <menuitem id="gym_menu_activities"
 52 +               name="Actividades"
 53 +               parent="gym_menu_root"
 54 +               action="gym_activity_action"
 55 +               sequence="10"/>
 56 + 
 57 + </odoo>
```

> El XML de vistas es donde más se nota la filosofía de Odoo: describes *qué quieres mostrar*, no *cómo dibujarlo*. Hay tres piezas:
> - **Vista árbol** (`<tree>`): la tabla/listado con columnas
> - **Vista formulario** (`<form>`): el detalle de un registro, con grupos que forman filas de campos
> - **Acción + Menús**: crean la entrada "Gimnasio > Actividades" en la barra de navegación de Odoo
>
> Si conoces HTML, piensa en esto como si escribieras solo el `<form>` con los `<input>` etiquetados, y Odoo se encargase automáticamente del CSS, la validación, los botones de guardar/cancelar, la paginación y la conexión a la base de datos.

---

✅ **Resultado final de este paso:** un módulo instalable que crea una tabla `gym_activity` en PostgreSQL y muestra en Odoo una pantalla funcional para gestionar actividades de gimnasio.
