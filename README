# README - Proyecto EcoFresh Canarias con Odoo y Docker

## Descripción del proyecto

Este proyecto consiste en la implementación de un entorno de gestión empresarial utilizando Odoo desplegado mediante Docker. El sistema está compuesto por dos servicios principales:

* **web**: contenedor que ejecuta la aplicación Odoo (interfaz web y lógica de negocio)
* **db**: contenedor que ejecuta PostgreSQL, donde se almacenan todos los datos de la empresa

El objetivo es disponer de un entorno portable, reproducible y fácil de mantener para la gestión empresarial.

---

## Estructura del proyecto

```
/proyecto-odoo
│
├── docker-compose.yml
├── docker-compose-persistent.yml
├── docker-compose-pgadmin.yml
├── guide/
├── assets/
│   ├── img/
│   └── registros/
├── addons/gym_addon/
│   ├── controllers/
│   ├── models/
│   ├── security/
│   ├── templates/
│   ├── views/
│   ├── __manifest__.py
│   └── __init__.py
├── db-backup/
│   ├── backup.sql
│   └── EcoFresh-DB_2026-05-01_20-44-12.zip
├── LICENSE
└── README.md
```

---

## Requisitos previos

* Docker Desktop instalado
* Docker Compose habilitado
* Navegador web

---

## Puesta en marcha del entorno

1. Abrir terminal en la carpeta del proyecto
2. Ejecutar:

```bash
docker compose up -d
```

3. Acceder a Odoo desde el navegador:

```
http://localhost:80
```

---

## Gestión de la base de datos

### Estructura

* La base de datos se ejecuta en el contenedor `db`
* Utiliza PostgreSQL
* El usuario por defecto suele ser: `odoo`

---

## Copias de seguridad (Backups)

Las copias de seguridad se almacenan en la carpeta:

```
/db-backup
```

Tipos de backup:

* `.sql` → exportación directa de PostgreSQL
* `.zip` → exportación desde Odoo (incluye adjuntos)

---

## Crear un backup manual

### Opción 1: desde Docker

```bash
docker compose exec db pg_dump -U odoo nombre_bd > db-backup/backup.sql
```

### Opción 2: desde Odoo

1. Ir a:

   ```
   http://localhost:80/web/database/manager
   ```
2. Seleccionar "Backup"
3. Descargar archivo `.zip`

---

## Restaurar la base de datos

### Opción 1: restaurar desde archivo .sql (recomendada en Docker)

1. Asegúrate de que los contenedores están en ejecución:

```bash
docker compose up -d
```

2. Restaurar el backup:

```bash
docker compose exec -T db psql -U odoo nombre_bd < db-backup/backup.sql
```

---

### Opción 2: restaurar desde Odoo (.zip)

1. Acceder a:

```
http://localhost:80/web/database/manager
```

2. Pulsar en "Restore"
3. Subir el archivo `.zip`
4. Introducir contraseña maestra

---

## Notas importantes

* El nombre de la base de datos (`nombre_bd`) debe existir antes de restaurar desde `.sql`
* Si no existe, puedes crearla con:

```bash
docker compose exec db createdb -U odoo nombre_bd
```

* Asegúrate de que los nombres coinciden exactamente

---

## Buenas prácticas

* Realizar backups periódicos
* Guardar copias fuera del entorno Docker
* Versionar solo configuraciones, no datos sensibles
* Verificar restauraciones en entornos de prueba

---

## Problemas comunes

### Error de conexión a la base de datos

* Verificar que el contenedor `db` está activo

### Error al restaurar

* Revisar nombre de base de datos
* Comprobar permisos del usuario `odoo`

### No aparecen datos

* Confirmar que el backup se ha restaurado correctamente

---

## Conclusión

Este entorno permite trabajar con Odoo de forma aislada y portable gracias a Docker. La correcta gestión de backups garantiza la seguridad de los datos y facilita la migración entre equipos.

---
