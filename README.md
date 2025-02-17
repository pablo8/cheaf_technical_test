# Cheaf Test Técnico

Este proyecto es una API desarrollada con **Django Rest Framework (DRF)**
que implementa autenticación con **JWT (JSON Web Tokens)** para la creación de usuarios y
la gestión de productos, alertas y endpoints protegidos.

Actualmente, permite la creación de usuarios y la autenticación mediante JWT.

---
## **Estructura del Proyecto**
```
cheaf_test_tecnico/
│── manage.py
│── .env  # Configuración de entorno
│── env_template  # Template de configuración de entorno
│── apps/
│   ├── core/  # Modelo de usuario y autenticación
│   ├── products/  # Modelo de productos y logica de negocio
│   ├── alerts/  # Modelo de alertas y logica de negocio
│── utils/  # Configuraciones adicionales
│── xscripts/ # Scripts adicionales
│── conftest.py # Archivo configuración tests
│── pytest.ini/ # Archivo configuracion tests
│── Dockerfile/ # Archivo configuracion de docker
│── docker-compose.yml/ # Archivo configuracion de volumenes y servicios
│── nginx.conf/ # Archivo configuracion de nginx (redireccionamiento de puerto para servir estaticos)
│── xscripts/ # Scripts adicionales
│── requirements.txt # Librerias del proyecto
```
¡Sí, es totalmente posible y de hecho es una **buena práctica**! 🚀  
Agregar una sección de **Tecnologías Utilizadas** ayuda a documentar las versiones exactas de herramientas y librerías, facilitando futuras actualizaciones y debugging.  

---

### **📌 Nueva Sección: Tecnologías Utilizadas**
Puedes agregar esta sección al **README** justo después de la introducción o antes de la configuración del entorno.  

---

## **🛠 Tecnologías Utilizadas**
Este proyecto utiliza las siguientes tecnologías y herramientas:

### **📌 Backend**
| Tecnología       | Versión  | Descripción |
|-----------------|----------|-------------|
| **Python**      | `3.10+`  | Lenguaje principal del backend. |
| **Django**      | `5.1.6`  | Framework web en el que está basado el proyecto. |
| **Django Rest Framework (DRF)** | `3.15.2` | Para construir la API REST. |

### **📌 Base de Datos y Caché**
| Tecnología       | Versión | Descripción |
|-----------------|---------|-------------|
| **PostgreSQL**  | `14+`   | Base de datos relacional. |
| **Redis**       | `5.2.1` | Almacenamiento en caché y broker de mensajes. |

### **📌 Mensajería y Tareas Asíncronas**
| Tecnología       | Versión | Descripción |
|-----------------|---------|-------------|
| **Celery**      | `5.4.0` | Manejo de tareas asíncronas en el backend. |
| **Redis**       | `5.2.1` | Usado como broker para Celery. |

### **📌 Infraestructura y Despliegue**
| Tecnología       | Versión          | Descripción |
|-----------------|------------------|-------------|
| **Docker**      | `24.4.0`        | Contenedores para facilitar la ejecución del proyecto. |
| **Fly.io**      | `Última versión` | Plataforma de despliegue para producción. |
| **GitHub Actions** | -                | CI/CD automatizado para despliegues. |

### **📌 Otras Herramientas**
| Tecnología       | Versión  | Descripción |
|-----------------|----------|-------------|
| **Gunicorn**    | `21.2.0` | Servidor WSGI para correr Django en producción. |

---

### **📌 ¿Cómo actualizar esta sección?**
1. Para ver las versiones instaladas de paquetes en el entorno actual:
   ```powershell
   pip freeze
   ```
2. Para ver la versión de **Docker**:
   ```powershell
   docker --version
   ```
3. Para ver la versión de **Fly.io CLI**:
   ```powershell
   flyctl version
   ```
4. Para ver la versión de **Redis** (si se está ejecutando como contenedor en Docker):
   ```powershell
   docker exec -it redis redis-cli INFO server | Select-String version
   ```

---

## Instalación

### **Requisitos Previos**
Antes de comenzar, asegúrate de tener instalado:
- **Python 3.8+**
- **PostgreSQL**
- **Docker Desktop (opcional)**
- **Virtualenv** (recomendado)

## ⚙️ Instalación y Configuración

### **Clonar el Repositorio**
```bash
git clone https://github.com/pablo8/cheaf_technical_test.git
cd cheaf_test_tecnico
```

### **Crear y Activar un Entorno Virtual**
```bash
python -m venv .venv  # Crear entorno virtual
source .venv/bin/activate  # Activar en macOS/Linux
.venv\Scripts\activate  # Activar en Windows
```

### **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **Configurar Variables de Entorno**
Crear un archivo `.env` en la raíz del proyecto y definir las siguientes variables:
```env
SECRET_KEY=tu_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
CORS_ORIGIN_WHITELIST=http://localhost,http://127.0.0.1
BASE_URL=http://localhost:8000
CLIENT_NAME=CheafTest
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cheaf
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
```

---

### **Base de Datos (PostgreSQL)**
Accede a PostgreSQL y ejecuta:
```sql
CREATE DATABASE cheaf;
```

### **Migraciones**
```bash
python manage.py makemigrations core
python manage.py migrate
```

---

## **Superusuario**
```bash
python manage.py createsuperuser
```

## **Iniciar el servidor**
```bash
python manage.py runserver  # Iniciar servidor
```

---

## **🔐 Autenticación JWT**

### **Obtener Token**
**Endpoint:** `POST /auth/token/`
```json
{
    "email": "testuser@example.com",
    "password": "securepassword123"
}
```
**Respuesta esperada:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```

### **Refrescar Token**
**Endpoint:** `POST /auth/token/refresh/`
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```
**Respuesta esperada:**
```json
{
    "access": "nuevo_access_token"
}
```

### **Verificar Token**
**Endpoint:** `POST /auth/token/verify/`
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```
**Si el token es válido, responde `200 OK`.**  
**Si el token es inválido, responde `401 Unauthorized`.**

---

## **Carga de Datos de Prueba**

Para facilitar las pruebas de la API, se crearon **dos scripts** en la carpeta `xscripts/` que permiten limpiar la base de datos y cargar datos de prueba utilizando la libreria `Faker`.  

### **Limpieza de la Base de Datos**
Antes de cargar datos nuevos, puedes limpiar la base de datos con:
```bash
python xscripts/clean_db.py
```

### **Carga Masiva de Datos**
Para generar datos de prueba, usa:
```bash
python xscripts/populate_db.py 1000  # Carga 1000 productos (2000 alertas)
python xscripts/populate_db.py 200000  # Carga 200,000 productos (400,000 alertas)
```
📌 **Nota:**  
La cantidad que ingreses como parámetro `n` definirá el número de productos creados.  
Cada producto tiene **2 alertas asociadas**, por lo que la cantidad total de alertas será `2 * n`.

---

## **Configuración de Redis con Docker en Windows**

### **Pasos para Configurar Redis en Docker Desktop**
1. **Descargar e Instalar Docker Desktop**  
   - 🔗 [Guía de instalación oficial](https://docs.docker.com/desktop/setup/install/windows-install/)  
   - Habilita la opción de **WSL 2 backend** durante la instalación.

2. **Configurar WSL con Ubuntu**  
   - Descarga una imagen de Ubuntu desde la **Microsoft Store**.
   - Abre Ubuntu desde PowerShell y configúrala con:
     ```bash
     sudo apt update && sudo apt upgrade -y
     ```

3. **Descargar e Iniciar un Contenedor de Redis**  
   ```bash
   docker run --name redis-server -d -p 6379:6379 redis
   ```

4. **Verificar que Redis Está Corriendo**  
   ```bash
   docker ps  # Ver los contenedores activos
   docker exec -it redis-server redis-cli ping  # Debería responder con "PONG"
   ```

5. **Configurar Django para Usar Redis**  
   Asegúrate de que en `settings.py` Redis esté configurado correctamente:
   ```python
   CACHES = {
       "default": {
           "BACKEND": "django_redis.cache.RedisCache",
           "LOCATION": "redis://localhost:6379/1",
           "OPTIONS": {
               "CLIENT_CLASS": "django_redis.client.DefaultClient",
           }
       }
   }
   ```
---

## **🔄 Configuración y Uso de Celery**

Este proyecto utiliza **Celery** para manejar tareas en segundo plano, como la actualización de alertas y el envío de notificaciones. La ejecución de estas tareas es gestionada por **Redis** como **message broker** y Celery Beat para programar tareas recurrentes.

---

### **📌 1️⃣ Instalación de Celery y Redis**
Antes de comenzar, asegúrate de que **Celery** y **Redis** están instalados en tu entorno virtual:

```bash
pip install celery django-celery-beat django-redis
```

---

### **📌 2️⃣ Configuración de Celery en Django**
📍 **En `settings.py`, agrega la configuración de Celery:**

```python
# Configuración de Redis como broker y backend
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
```

📍 **En `apps/core/celery.py` crea la configuración de Celery:**

```python
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaf_test_tecnico.settings")

app = Celery("cheaf_test_tecnico")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

📍 **En `apps/core/__init__.py` importa Celery para que Django lo reconozca:**

```bash
from .celery import app as celery_app

__all__ = ("celery_app",)
```

---

### **📌 3️⃣ Iniciar el Worker de Celery**
Para ejecutar Celery en Windows sin problemas de **multihilos**, usa el `--pool=solo`:

```bash
celery -A apps.core worker --pool=solo --loglevel=info
```

📌 **Si estás en Linux/macOS**, puedes ejecutar:

```bash
celery -A apps.core worker --loglevel=info
```

---

### **📌 4️⃣ Configurar Tareas Automáticas con Celery Beat**
Celery Beat se usa para programar tareas automáticas, como actualizar alertas y enviar notificaciones.

📍 **Añade Celery Beat a `INSTALLED_APPS` en `settings.py`:**

```bash
INSTALLED_APPS = [
    ...
    "django_celery_beat",
]
```

📍 **Ejecuta migraciones para Celery Beat:**
```bash
python manage.py migrate django_celery_beat
```

📍 **En `apps/core/celery.py`, agrega la configuración de tareas programadas:**
```bash
from celery.schedules import crontab

app.conf.beat_schedule = {
    "update_alerts_daily": {
        "task": "apps.alerts.tasks.update_alerts",
        "schedule": crontab(hour=0, minute=0),  # Ejecutar a la medianoche
    },
    "send_notifications_daily": {
        "task": "apps.alerts.tasks.notify_products_before_expiration",
        "schedule": crontab(hour=0, minute=0),  # Ejecutar a la medianoche
    },
}
```

📌 **Ejecutar Celery Beat en otra terminal para activar las tareas programadas:**
```bash
celery -A apps.core beat --loglevel=info
```

---

### **📌 6️⃣ Comandos Útiles de Celery**
📍 **Ejecutar una tarea manualmente**:
```bash
celery -A apps.core call apps.alerts.tasks.update_alerts
```

📍 **Obtener el resultado de una tarea específica**:
```bash
celery -A apps.core result <TASK_ID>
```

📍 **Ver el estado de los workers activos**:
```bash
celery -A apps.core inspect active
```

📍 **Ver las tareas en cola**:
```bash
celery -A apps.core inspect reserved
```

📍 **Ver las tareas programadas**:
```bash
celery -A apps.core inspect scheduled
```

📍 **Iniciar Celery en modo depuración**:
```bash
celery -A apps.core worker --loglevel=debug
```

---

### **📌 7️⃣ Probar Celery en Desarrollo**
Si quieres probar si Celery está ejecutando tareas correctamente:

1️⃣ **Ejecuta Redis en Docker Desktop** (si no lo tienes corriendo):
```bash
docker run --name redis-server -d -p 6379:6379 redis
```

2️⃣ **Ejecuta Celery Worker en una terminal:**
```bash
celery -A apps.core worker --pool=solo --loglevel=info
```

3️⃣ **Ejecuta Celery Beat en otra terminal:**
```bash
celery -A apps.core beat --loglevel=info
```

4️⃣ **Fuerza la ejecución de la tarea de actualización de alertas:**
```bash
celery -A apps.core call apps.alerts.tasks.update_alerts
```

5️⃣ **Verifica en la base de datos si las alertas se actualizaron.**

---

## **🔔 Configuración de Notificaciones por Correo con Mailhog**

Para las notificaciones de productos por caducar, se ha configurado **Mailhog** como servidor de pruebas para envíos de correo.

### **1️⃣ Instalación y Configuración de Mailhog**
Mailhog es una herramienta que permite capturar correos electrónicos en un entorno de desarrollo sin necesidad de configurar un servidor SMTP real.

📌 **Pasos para configurar Mailhog con Docker:**
```bash
docker run --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog
```
Esto iniciará Mailhog y estará disponible en:
- **SMTP:** `localhost:1025`
- **Interfaz Web:** [http://localhost:8025](http://localhost:8025)

📌 **Configuración en `settings.py`**
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = "noreply@cheaf.com"
```

---

### **2️⃣ Creación de la tarea de Celery para Notificaciones**
Cuando un producto está a punto de vencer, se envía un correo electrónico a los usuarios de pruebas, 
definidos genéricamente como `testusernotiX@test.com` y la alerta cambia de estado a **expirada**.

---

### **3️⃣ Prueba de la Tarea de Notificaciones con Celery y Mailhog**
📌 **Ejecutar Celery Worker**
Antes de ejecutar la tarea, inicia el worker de Celery:
```bash
celery -A apps.core worker --pool=solo --loglevel=info
```

📌 **Ejecutar la tarea manualmente**
Puedes probar la tarea en Celery llamándola directamente:
```bash
celery -A apps.core call apps.alerts.tasks.send_alert_notifications --args='[1,2,3,4,5]'
```
(Sustituye `[1,2,3,4,5]` por IDs de alertas activas que quieras notificar).

📌 **Verificar correos en Mailhog**
Accede a [http://localhost:8025](http://localhost:8025) y revisa los correos enviados.

---

### **4️⃣ Programación Automática de la Tarea con Celery Beat**

📌 **Instalar Celery Beat**
```bash
pip install django-celery-beat
```

📌 **Agregarlo en `INSTALLED_APPS` de `settings.py`**
```python
INSTALLED_APPS = [
    ...,
    'django_celery_beat',
]
```

📌 **Migrar Base de Datos**
```bash
python manage.py migrate django_celery_beat
```

📌 **Ejecutar Celery Beat**
```bash
celery -A apps.core beat --loglevel=info
```

📌 **Ejecutar Celery Worker**
```bash
celery -A apps.core worker --pool=solo --loglevel=info
```

---

## **🛠️ Pruebas Unitarias con Pytest**

Para garantizar la estabilidad del código, se han implementado **pruebas unitarias** con **pytest**.  
Las pruebas están ubicadas en la carpeta de cada aplicación (`apps/products/tests.py`, `apps/alerts/tests.py`, etc.).

### **📌 Configuración de Pytest**

1. **Instalar pytest y pytest-django**  
   Asegúrate de que estas dependencias estén instaladas:
   ```bash
   pip install pytest pytest-django
   ```
   
2. **Archivo de configuración `pytest.ini`**  
   Para que pytest reconozca Django, agrega un archivo `pytest.ini` en la raíz del proyecto:
   ```ini
   [pytest]
   DJANGO_SETTINGS_MODULE = cheaf_test_tecnico.settings
   python_files = tests.py test_*.py *_tests.py
   ```

3. **Configuración de `conftest.py`**  
   En la raíz del proyecto, crea un archivo `conftest.py` para inicializar Django antes de ejecutar pruebas:
   ```python
   import os
   import django

   def pytest_configure():
       """Configura Django antes de ejecutar cualquier test"""
       os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheaf_test_tecnico.settings')
       django.setup()
   ```

### **📌 Cómo Ejecutar las Pruebas**
Ejecutar todas las pruebas:
```bash
pytest
```
Ejecutar pruebas en una aplicación específica (`products`):
```bash
pytest apps/products/
```
Ejecutar un solo archivo de prueba:
```bash
pytest apps/products/tests.py
```
Ejecutar una prueba específica dentro de un archivo:
```bash
pytest apps/products/tests.py::test_nombre_funcion
```
Ejecutar pruebas con información detallada:
```bash
pytest -v
```
Ejecutar pruebas y generar reporte de cobertura:
```bash
pytest --cov=apps
```

### **📌 Estructura de los Tests**
Cada aplicación tiene su propio archivo `tests.py` con pruebas unitarias:
```
apps/
│── products/
│   ├── models.py
│   ├── views.py
│   ├── tests.py  <-- Pruebas unitarias de productos
│── alerts/
│   ├── models.py
│   ├── views.py
│   ├── tests.py  <-- Pruebas unitarias de alertas
```

### **📌 Qué Pruebas Se Implementaron**
1. **Pruebas de `Product`:**
   - Creación de productos.
   - Validación de fechas de expiración.
   - Relaciones con alertas.
   - Pruebas de métodos personalizados en `ProductManager`.

2. **Pruebas de `Alert`:**
   - Creación de alertas.
   - Cálculo de `days_to_activation` y `days_since_activation`.
   - Cambio de estado cuando una alerta vence (`STATUS_EXPIRED_ID`).
   - Envío de notificaciones cuando un producto está por caducar.

---

## 🚀 **Dockerización del Proyecto**

Este proyecto está **dockerizado** para facilitar la configuración y despliegue. Con **Docker Compose**, puedes levantar toda la aplicación (Django, PostgreSQL, Redis, Celery, Nginx, MailHog) en cuestión de segundos.

---

### 🛠 **1. Requisitos Previos**
Antes de comenzar, asegúrate de tener instalado:

- **[Docker Desktop](https://www.docker.com/products/docker-desktop)**
- **[Docker Compose](https://docs.docker.com/compose/)** (Incluido en Docker Desktop)
- **Variable (en settings) `USING_DOCKER_CONFIG = True` **

---

### 🏗 **2. Construcción de los Contenedores**
Para construir los contenedores y preparar la aplicación, ejecuta:


```sh
docker-compose build
```

---

### 🚀 **3. Levantar el Proyecto**
Una vez construidos los contenedores, inicia la aplicación con:

```sh
docker-compose up -d
```

Esto iniciará los siguientes servicios:
- **web** → Contenedor con Django y Gunicorn.
- **db** → PostgreSQL como base de datos.
- **redis** → Cache y cola de tareas para Celery.
- **celery_worker** → Procesador de tareas en segundo plano.
- **nginx** → Servidor de archivos estáticos y proxy reverso.
- **mailhog** → Servidor de pruebas para emails.

---

### 📌 **4. Verificar que Todo Funciona**
Puedes verificar los contenedores corriendo con:

```sh
docker ps
```

También puedes ver los logs de un contenedor específico, por ejemplo, de **web**:

```sh
docker-compose logs web
```

---

### 🛠 **5. Ejecutar Migraciones y Crear un Superusuario**
Antes de poder usar la aplicación, debes aplicar las migraciones y crear un superusuario.

#### **Aplicar Migraciones**
```sh
docker-compose exec web python manage.py migrate
```

#### **Crear un Superusuario**
```sh
docker-compose exec web python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para configurar el usuario administrador.

---

### 🛑 **6. Apagar el Proyecto**
Para detener la ejecución de los contenedores sin eliminarlos:

```sh
docker-compose down
```

Si quieres eliminar completamente los contenedores, volúmenes y datos:

```sh
docker-compose down -v
```

---

### 🛠 **7. Reconstruir un Servicio Específico**
Si necesitas reconstruir solo un servicio (por ejemplo, el de Django):

```sh
docker-compose build web
docker-compose up -d web
```

---

### 📂 **Estructura de Volúmenes**
Los datos de la base de datos y los archivos estáticos se almacenan en volúmenes para persistencia:

- PostgreSQL → `postgres_data`
- Archivos estáticos → `static_volume`
- Archivos multimedia → `media_volume`

Si necesitas limpiar completamente los datos almacenados en estos volúmenes:

```sh
docker volume rm cheaf_test_tecnico_postgres_data cheaf_test_tecnico_static_volume cheaf_test_tecnico_media_volume
```

---

### 🔄 **8. Recolectar Archivos Estáticos**
Para que Nginx pueda servir correctamente los archivos estáticos:

```sh
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart nginx
```

---

### 📬 **9. Pruebas de Emails con MailHog**
Si necesitas probar el envío de emails sin configurar un servidor real, **MailHog** estará corriendo en:

📌 **Accede a MailHog desde el navegador:**  
👉 [http://localhost:8025](http://localhost:8025)

Aquí podrás ver todos los correos enviados desde la aplicación.

---

### **📌 Comandos Útiles**
| Acción | Comando |
|---------|----------------------------|
| **Construir contenedores** | `docker-compose build` |
| **Levantar el proyecto** | `docker-compose up -d` |
| **Ver logs de un contenedor** | `docker-compose logs <servicio>` |
| **Ejecutar migraciones** | `docker-compose exec web python manage.py migrate` |
| **Crear superusuario** | `docker-compose exec web python manage.py createsuperuser` |
| **Detener los contenedores** | `docker-compose down` |
| **Eliminar contenedores y volúmenes** | `docker-compose down -v` |
| **Reconstruir solo un servicio** | `docker-compose build web && docker-compose up -d web` |
| **Reiniciar Nginx** | `docker-compose restart nginx` |
| **Acceder a MailHog** | `http://localhost:8025` |


---

## ✅ **Proceso Manual para Probar la Simulación en Local con Redis en Docker**
Si estás ejecutando **Redis en Docker Desktop**, no puedes ejecutar Celery desde la consola sin conflictos. Por eso, sigues este flujo:

### 🔹 **Pasos para Probar la Simulación Localmente**
```sh
1. python xscripts/clean_db.py         # Limpia la base de datos
2. python xscripts/populate_db.py      # Población inicial de datos
3. docker start redis-server           # Inicia Redis dentro de Docker
4. celery -A apps.core worker --pool=solo --loglevel=info  # Inicia Celery Worker
5. celery -A apps.core call apps.alerts.tasks.simulate_notifications  # Lanza la simulación
```
---
### 🔹 **Para Finalizar el Worker y Limpiar Redis**
```sh
6. celery -A apps.core purge           # Limpia la cola de tareas en Celery
7. Repetir los pasos (1 y 2) para reiniciar la base de datos antes de una nueva prueba
```

---


### **📌 Configuración de Fly.io en Windows**
Este proyecto está configurado para desplegarse en **Fly.io**. A continuación, se detallan los pasos para instalar Fly.io, configurar la base de datos, ejecutar migraciones y hacer el despliegue.

---

## **1️⃣ Instalación de Fly.io en Windows**
Ejecutar el siguiente comando en **PowerShell** (como administrador) para instalar Fly.io CLI:

```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Para verificar que se instaló correctamente:

```powershell
flyctl version
```

---

## **2️⃣ Autenticarse en Fly.io**
Para iniciar sesión en Fly.io, ejecutar:

```powershell
flyctl auth login
```

Esto abrirá el navegador para iniciar sesión con la cuenta de Fly.io.

---

## **3️⃣ Crear la Aplicación en Fly.io**
Antes de ejecutar este comando, **es obligatorio estar en la raíz del proyecto**.

```powershell
flyctl launch
```

Durante el proceso, Fly.io pedirá:
- **Nombre de la aplicación** (puedes aceptar el nombre generado o escribir uno personalizado).
- **Región** (seleccionar la más cercana, por ejemplo, `iad` para EE.UU. o `gru` para Brasil).
- **Configuración automática** de base de datos y otros servicios.

Esto generará automáticamente el archivo **`fly.toml`**, que contiene la configuración de despliegue.

---

## **4️⃣ Crear una Base de Datos en Fly.io**
Si el proyecto usa PostgreSQL, se puede crear con el siguiente comando:

```powershell
flyctl postgres create
```

Para asociar la base de datos a la aplicación:

```powershell
flyctl postgres attach --app <nombre-de-la-app>
```

Para verificar las variables de entorno disponibles en Fly.io:

```powershell
flyctl secrets list --app <nombre-de-la-app>
```

---

## **5️⃣ Configurar el Token de Fly.io en GitHub**
GitHub Actions necesita autenticarse en Fly.io para desplegar automáticamente la aplicación.  

1. Obtener el token de Fly.io con:
   ```powershell
   flyctl auth token
   ```
2. **Copiar el token generado**.
3. **Ir al repositorio en GitHub → "Settings" → "Secrets and variables" → "Actions".**
4. **Crear un nuevo secreto llamado `FLY_API_TOKEN`** y pegar el valor copiado.

---

## **6️⃣ Configurar Archivos Estáticos en Django**
Cuando `DEBUG = False`, Django **no sirve archivos estáticos automáticamente**. Para solucionarlo:

1️⃣ **Ejecutar `collectstatic` en Fly.io para recopilar los archivos estáticos:**
```powershell
flyctl ssh console --app <nombre-de-la-app>
```
Luego, dentro de la terminal de Fly.io:
```bash
python manage.py collectstatic --noinput
exit
```

2️⃣ **Configurar `fly.toml` para servir estáticos:**
Abrir `fly.toml` y agregar dentro de `[http_service]`:

```toml
[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.routes]]
    handle_path = "/static/*"
    root = "/app/static/"
```

---

## ** Desplegar la Aplicación**
Para hacer el despliegue manualmente en Fly.io:

```powershell
flyctl deploy
```

Para abrir la aplicación en el navegador:

```powershell
flyctl open
```

Para ver los logs en tiempo real:

```powershell
flyctl logs --app <nombre-de-la-app>
```

---

## **📌 Resumen Final**
1️⃣ **Instalar Fly.io CLI** (`iwr https://fly.io/install.ps1 -useb | iex`).  
2️⃣ **Autenticarse en Fly.io** (`flyctl auth login`).  
3️⃣ **Crear la aplicación en Fly.io** (`flyctl launch`).  
4️⃣ **Configurar PostgreSQL en Fly.io** (`flyctl postgres create`).  
5️⃣ **Configurar el Token en GitHub Secrets (`FLY_API_TOKEN`).**  
6️⃣ **Configurar archivos estáticos con WhiteNoise** (`pip install whitenoise`).  
7️⃣ **Ejecutar `collectstatic` y modificar `fly.toml`**.  
8️⃣ **Hacer `git push` y desplegar la aplicación (`flyctl deploy`).**  

---

**Este README será actualizado conforme avance el proyecto.** 🚀

