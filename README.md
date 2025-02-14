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

---

## **Próximos Pasos**
✅ Implementar **CRONJOB** para calcular los días restantes y pasados de la alerta.  
✅ **Dockerización** del proyecto.  
✅ Configurar **CI/CD** para automatizar despliegues (definir servidor web).  

---

**Este README será actualizado conforme avance el proyecto.** 🚀

