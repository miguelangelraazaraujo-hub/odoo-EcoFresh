# 🌐 Paso 4 de 4 — `_4_controladores`

**Objetivo:** Exponer el horario del gimnasio como una página web pública, accesible desde cualquier navegador sin necesidad de estar registrado en Odoo, introduciendo el patrón MVC con controladores HTTP.

---

## 🧠 ¿Qué se hizo y por qué tiene sentido aquí?

Hasta ahora todo lo construido vive dentro del backoffice de Odoo: solo lo ven los empleados con acceso al panel de administración. En este último paso se da el salto hacia afuera: se crea una URL pública (`/gym/schedule`) que cualquier visitante puede abrir en el navegador y ver el horario semanal del gimnasio.

Para ello Odoo usa el patrón **MVC** (Modelo - Vista - Controlador), exactamente igual que en frameworks web que ya conoces (Spring MVC en Java, Express en Node.js):

| Pieza | Aquí | Rol |
|---|---|---|
| **Modelo** | `gym.schedule` (ya existía) | Los datos en BD |
| **Controlador** | `controllers/portal.py` | Recibe la petición HTTP, consulta los datos, los prepara |
| **Vista** | `templates/portal_schedule.xml` | El HTML que se renderiza y se devuelve al navegador |

La novedad frente a pasos anteriores es que el XML ya no describe pantallas de backoffice sino HTML real con bucles y condicionales, usando el motor de plantillas **QWeb** de Odoo.

---

## 🗁 Vista general de ficheros

```
addons/gym_addon/
├── 🟡 __init__.py
├── 🟡 __manifest__.py
├── controllers/
│   ├── 🟢 __init__.py
│   └── 🟢 portal.py
└── templates/
    └── 🟢 portal_schedule.xml
```

🟢 Nuevo &nbsp;&nbsp; 🟡 Modificado &nbsp;&nbsp; 🔴 Eliminado

---

## 🗂️ Archivos afectados

### `addons/gym_addon/controllers/__init__.py` — 🟢 NUEVO

```diff
  1 + from . import portal
```

> Mismo patrón de siempre: hace que la carpeta `controllers` sea un paquete Python y carga `portal.py`.

---

### `addons/gym_addon/controllers/portal.py` — 🟢 NUEVO

```diff
  1 + from odoo import http
  2 + from odoo.http import request
  3 + 
  4 + 
  5 + class GymPortalController(http.Controller):
  6 + 
  7 +     @http.route('/gym/schedule', type='http', auth='public', website=True)
  8 +     def public_schedule(self):
  8 +         """
  9 +         auth='public' → no requiere login.
 10 +         """
 11 +         # Recuperamos todos los horarios ordenados por día y hora
 12 +         schedules = request.env['gym.schedule'].sudo().search(
 13 +             [],
 14 +             order='day_of_week, time_start',
 15 +         )
 16 + 
 17 +         # Agrupamos por día para facilitar el renderizado
 18 +         days = {
 19 +             '0': 'Lunes', '1': 'Martes', '2': 'Miércoles',
 20 +             '3': 'Jueves', '4': 'Viernes', '5': 'Sábado', '6': 'Domingo',
 21 +         }
 22 +         schedule_by_day = {}
 23 +         for slot in schedules:
 24 +             day_label = days.get(slot.day_of_week, slot.day_of_week)
 25 +             schedule_by_day.setdefault(day_label, []).append(slot)
 26 + 
 27 +         return request.render(
 28 +             'gym_addon.portal_schedule_public',
 29 +             {
 30 +                 'schedule_by_day': schedule_by_day,
 31 +                 'days_order': list(days.values()),
 32 +             },
 33 +         )
```

> Desglosando las piezas clave:
> - `@http.route('/gym/schedule', ...)` — el decorador que registra la URL, igual que `@GetMapping("/gym/schedule")` en Spring o `app.get('/gym/schedule', ...)` en Express.
> - `auth='public'` — no requiere login; cualquier visitante puede acceder.
> - `request.env['gym.schedule'].sudo().search([])` — consulta todos los horarios. `.sudo()` eleva los permisos para poder leer aunque el visitante no esté autenticado. `search([])` con lista vacía equivale a `SELECT * FROM gym_schedule`.
> - `schedule_by_day.setdefault(day_label, []).append(slot)` — agrupa los horarios en un diccionario `{ "Lunes": [slot1, slot2], "Martes": [...] }` para que la plantilla pueda iterar por días fácilmente.
> - `request.render(...)` — devuelve la plantilla renderizada con los datos, como un `return ModelAndView(...)` en Spring MVC.

---

### `addons/gym_addon/templates/portal_schedule.xml` — 🟢 NUEVO

```diff
  1 + <?xml version="1.0" encoding="utf-8"?>
  2 + <odoo>
  3 + 
  4 +     <template id="portal_schedule_public" name="Horario Semanal Público">
  5 +         <t t-call="website.layout">
  6 +             <div class="container mt-4">
  7 + 
  8 +                 <h1 class="mb-4">Horario Semanal</h1>
  9 + 
  10 +                 <t t-foreach="days_order" t-as="day">
  11 +                     <t t-if="schedule_by_day.get(day)">
  12 +                         <h3 class="mt-4">
  13 +                             <t t-esc="day"/>
  14 +                         </h3>
  15 +                         <table class="table table-bordered table-hover">
  16 +                             <thead class="table-dark">
  17 +                                 <tr>
  18 +                                     <th>Actividad</th>
  19 +                                     <th>Inicio</th>
  20 +                                     <th>Fin</th>
  21 +                                     <th>Monitor/a</th>
  22 +                                     <th>Plazas</th>
  23 +                                 </tr>
  24 +                             </thead>
  25 +                             <tbody>
  26 +                                 <t t-foreach="schedule_by_day[day]" t-as="slot">
  27 +                                     <tr>
  28 +                                         <td><t t-esc="slot.activity_id.name"/></td>
  29 +                                         <td><t t-esc="'%02d:%02d' % (int(slot.time_start), int((slot.time_start % 1) * 60))"/></td>
  30 +                                         <td><t t-esc="'%02d:%02d' % (int(slot.time_end),   int((slot.time_end   % 1) * 60))"/></td>
  31 +                                         <td><t t-esc="slot.instructor or '-'"/></td>
  32 +                                         <td><t t-esc="slot.activity_id.max_capacity"/></td>
  33 +                                     </tr>
  34 +                                 </t>
  35 +                             </tbody>
  36 +                         </table>
  37 +                     </t>
  38 +                 </t>
  39 + 
  40 +                 <p t-if="not schedule_by_day" class="text-muted">
  41 +                     No hay actividades programadas esta semana.
  42 +                 </p>
  43 + 
  44 +             </div>
  45 +         </t>
  46 +     </template>
  47 + 
  48 + </odoo>
```

> Esta plantilla usa **QWeb**, el motor de plantillas de Odoo. Si conoces Thymeleaf, Jinja2 o Handlebars, la sintaxis es muy similar. Las directivas clave son:
> - `t-call="website.layout"` — hereda la cabecera y pie de página del sitio web de Odoo, como extender un layout base en cualquier otro framework.
> - `t-foreach="days_order" t-as="day"` — bucle. Equivale a `{% for day in days_order %}` en Jinja2 o `th:each` en Thymeleaf.
> - `t-if="schedule_by_day.get(day)"` — condicional. Solo renderiza la tabla de un día si ese día tiene horarios.
> - `t-esc="slot.activity_id.name"` — imprime el valor escapando HTML para evitar XSS, como `{{ }}` en otros motores.
> - La expresión `'%02d:%02d' % (int(slot.time_start), ...)` convierte el `Float` 9.5 en el string `"09:30"` directamente en la plantilla.
> - Las clases CSS (`table`, `table-bordered`, `container`, etc.) son de **Bootstrap**, que Odoo ya incluye por defecto.

---

### `addons/gym_addon/__init__.py` — 🟡 MODIFICADO

```diff
  1   from . import models
  2 + from . import controllers
```

> Se registra el nuevo paquete `controllers` para que Python lo cargue al arrancar el addon.

---

### `addons/gym_addon/__manifest__.py` — 🟡 MODIFICADO

```diff
  8 -    'depends': ['base'],
  9 +    'depends': ['base', 'portal', 'website'],
 10 
 11      'data': [
 12          'security/ir.model.access.csv',
 13          'views/gym_activity_views.xml',
 14          'views/gym_schedule_views.xml',
 15 +        'templates/portal_schedule.xml',
 16      ],
 17 -    'version': '17.0.3.0.0',
 18 +    'version': '17.0.4.0.0',
```

> Se añaden dos nuevas dependencias: `portal` (gestión de usuarios públicos) y `website` (el CMS de Odoo que proporciona el layout web, el enrutador HTTP y Bootstrap). Sin ellas, `t-call="website.layout"` y `auth='public'` no estarían disponibles.

---

✅ **Resultado final de este paso — y del proyecto completo:** al visitar `http://localhost/gym/schedule` en el navegador, cualquier persona (sin login) ve el horario semanal del gimnasio organizado por días, con tablas Bootstrap, dentro del layout del sitio web de Odoo. Los datos son en tiempo real: cualquier cambio en el backoffice se refleja inmediatamente en la página pública.
