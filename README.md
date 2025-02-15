# Cheaf Test Técnico

Este proyecto es una API desarrollada con **Django Rest Framework (DRF)**
que implementa autenticación con **JWT (JSON Web Tokens)** para la creación de usuarios y
la gestión de productos, alertas y endpoints protegidos.

Actualmente, permite la creación de usuarios y la autenticación mediante JWT.

---

## Instalación

### **Requisitos Previos**
Antes de comenzar, asegúrate de tener instalado:
- **Python 3.8+**
- **PostgreSQL**
- **Virtualenv** (opcional pero recomendado)

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

## **Configuración de la Base de Datos**
### **Crear la Base de Datos en PostgreSQL**
Accede a PostgreSQL y ejecuta:
```sql
CREATE DATABASE cheaf;
```

### **Aplicar Migraciones**
```bash
python manage.py makemigrations core
python manage.py migrate
```

---

## **Crear un Superusuario**
Para acceder al **admin de Django**:
```bash
python manage.py createsuperuser
```
Sigue las instrucciones e ingresa un email, nombre y contraseña.

---

## **Autenticación con JWT**
Este proyecto usa **JSON Web Tokens (JWT)** para la autenticación de usuarios.

### **Obtener Access Token**
**Endpoint:** `POST /api/token/`
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

### **Refrescar Access Token**
**Endpoint:** `POST /api/token/refresh/`
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
**Endpoint:** `POST /api/token/verify/`
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```
**Si el token es válido, responde `200 OK`.**  
**Si el token es inválido, responde `401 Unauthorized`.**

---

## **Estructura del Proyecto**
```
cheaf_test_tecnico/
│── manage.py
│── .env  # Configuración de entorno
│── apps/
│   ├── core/  # Modelo de usuario y autenticación
│   ├── products/  # Próximamente
│   ├── alerts/  # Próximamente
│── utils/  # Configuraciones adicionales
│── requirements.txt
```

---

## **Comandos ## **Comandos \u00dátiles**
```bash
python manage.py runserver  # Iniciar servidor
python manage.py createsuperuser  # Crear superusuario
python manage.py migrate  # Aplicar migraciones
```

---

## **Carga de Datos de Prueba**

Para facilitar las pruebas de la API, hemos creado **dos scripts** en la carpeta `xscripts/` que permiten limpiar la base de datos y cargar datos de prueba con `Faker`.  

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
¡Claro! Aquí tienes la **sección de Celery completamente integrada en tu README**, con todos los comandos relevantes, incluyendo la configuración del worker, el uso de `pool=solo` en Windows, Celery Beat y la programación de tareas automáticas. 

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

```python
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

```python
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
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    "update_alerts_daily": {
        "task": "apps.alerts.tasks.update_alerts",
        "schedule": crontab(hour=0, minute=0),  # Ejecutar a la medianoche
    },
    "send_notifications_daily": {
        "task": "apps.alerts.tasks.send_alert_notifications",
        "schedule": crontab(hour=8, minute=0),  # Ejecutar a las 8 AM
    },
}
```

📌 **Ejecutar Celery Beat en otra terminal para activar las tareas programadas:**
```bash
celery -A apps.core beat --loglevel=info
```

---

### **📌 5️⃣ Lista de Tareas en Celery**
📍 **En `apps/alerts/tasks.py`, define las tareas que se ejecutarán automáticamente:**

#### **✅ 5.1 Tarea para actualizar las alertas**
```python
@shared_task
def update_alerts():
    """Tarea programada para actualizar los días de activación de alertas."""
    today = now().date()
    alerts = Alert.objects.filter(status=STATUS_ACTIVE_ID)

    updated_alerts = 0
    for alert in alerts:
        alert.update_days()
        alert.save()
        updated_alerts += 1

    return f"Updated {updated_alerts} alerts."
```

#### **✅ 5.2 Tarea para enviar notificaciones**
```python
@shared_task
def send_alert_notifications():
    """Tarea para notificar a los usuarios sobre productos próximos a caducar."""
    today = now().date()
    alerts_to_notify = Alert.objects.filter(activation_date__date=today, status=STATUS_ACTIVE_ID)

    if not alerts_to_notify.exists():
        return "No alerts to notify today."

    for alert in alerts_to_notify:
        # Simulación de emails de prueba
        test_users = ["testuser1@example.com", "testuser2@example.com"]

        send_mail(
            f"📢 ¡Atención! El producto {alert.product.name} está por caducar",
            f"El producto {alert.product.name} caduca el {alert.product.expiration_date.strftime('%d/%m/%Y')}.",
            settings.DEFAULT_FROM_EMAIL,
            test_users,
        )

        alert.status = STATUS_EXPIRED_ID
        alert.save()

    return f"Notified {alerts_to_notify.count()} alerts today."
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

Aquí está la sección actualizada de **Mailhog y notificaciones con Celery** para agregar al **README**.

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
Cuando un producto está a punto de vencer, se envía un correo electrónico a los usuarios de prueba (`is_staff=True`) y la alerta cambia de estado a **expirada**.

📌 **Tarea de Celery (`apps/alerts/tasks.py`):**
```python
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from apps.alerts.models import Alert
from apps.core.models import User
from utils.constants import STATUS_ACTIVE_ID, STATUS_EXPIRED_ID

@shared_task
def send_alert_notifications(alert_ids):
    """
    Tarea programada para enviar notificaciones a usuarios cuando una alerta vence
    y actualizar el estado de la alerta a `STATUS_EXPIRED_ID`.
    """
    alerts = Alert.objects.filter(id__in=alert_ids, status=STATUS_ACTIVE_ID)

    if not alerts.exists():
        return "No hay alertas para notificar"

    # Obtener usuarios de prueba
    test_users = list(User.objects.filter(is_staff=True).values_list("email", flat=True))

    if not test_users:
        return "No hay usuarios de prueba para notificar"

    # Construir el cuerpo del email
    email_subject = "🔔 Productos por vencer"
    email_body = "📢 Atención: Los siguientes productos están por caducar:\n\n"
    email_body += "\n".join(
        [f"- {alert.product.name} (Expira: {alert.activation_date.strftime('%d/%m/%Y')})" for alert in alerts]
    )
    email_body += "\n\n📌 Por favor, revisa los productos antes de su expiración."

    # Enviar correo
    try:
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=test_users,
            fail_silently=False
        )
    except Exception as e:
        return f"Error enviando notificaciones: {str(e)}"

    # Actualizar estado de las alertas a expiradas
    alerts.update(status=STATUS_EXPIRED_ID)

    return f"Notificaciones enviadas correctamente a {len(test_users)} usuarios y {alerts.count()} alertas actualizadas."
```

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
Si quieres ejecutar la tarea automáticamente cada 24 horas, usa **Celery Beat**.

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

📌 **Configurar la Tarea en `apps/alerts/tasks.py`**
```python
from celery.schedules import crontab
from celery import Celery
from apps.alerts.tasks import send_alert_notifications

app = Celery("cheaf_test_tecnico")

app.conf.beat_schedule = {
    "send-alerts-daily": {
        "task": "apps.alerts.tasks.send_alert_notifications",
        "schedule": crontab(hour=0, minute=0),  # Ejecuta a medianoche
        "args": (),
    },
}
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

## **Próximos Pasos**
✅ **Dockerización** del proyecto.  
✅ Configurar **CI/CD** para automatizar despliegues (definir servidor web).  

---

**Este README será actualizado conforme avance el proyecto.** 🚀

