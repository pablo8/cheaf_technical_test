# Cheaf Test Técnico

Este proyecto es una API desarrollada con **Django Rest Framework (DRF)** 
que implementa autenticación con **JWT (JSON Web Tokens)** para la creación de usuarios y 
la gestión de productos, alertas y endpoints protegidos. 

Actualmente, permite la creación de usuarios y la autenticación mediante JWT.

## Instalación

### Requisitos Previos
Antes de comenzar, asegúrate de tener instalado:
- **Python 3.8+**
- **PostgreSQL**
- **Virtualenv** (opcional pero recomendado)

### Clonar el Repositorio
```bash
git clone https://github.com/pablo8/cheaf_technical_test.git
cd cheaf_test_tecnico
```

### Crear y Activar un Entorno Virtual
```bash
python -m venv .venv  # Crear entorno virtual
source .venv/bin/activate  # Activar en macOS/Linux
.venv\Scripts\activate  # Activar en Windows
```

### Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Configurar Variables de Entorno
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

## Configuración de la Base de Datos
### Crear la base de datos en PostgreSQL
Accede a PostgreSQL y ejecuta:
```sql
CREATE DATABASE cheaf;
```

### Aplicar Migraciones
```bash
python manage.py makemigrations core
python manage.py migrate
```

## Crear un Superusuario
Para acceder al admin de Django:
```bash
python manage.py createsuperuser
```
Sigue las instrucciones e ingresa un email, nombre y contraseña.

## Autenticación con JWT
Este proyecto usa **JSON Web Tokens (JWT)** para la autenticación de usuarios.

### Obtener Access Token
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

### Refrescar Access Token
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

### Verificar Token
**Endpoint:** `POST /api/token/verify/`
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI..."
}
```
**Si el token es válido, responde `200 OK`.**
**Si el token es inválido, responde `401 Unauthorized`.**

## Estructura del Proyecto
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

## Comandos Útiles
```bash
python manage.py runserver  # Iniciar servidor
python manage.py createsuperuser  # Crear superusuario
python manage.py migrate  # Aplicar migraciones
```

## Próximos Pasos
✅ Configurar el modelo de negocio y endpoints adicionales.
✅ Integrar lógica para `products` y `alerts`.
✅ Mejorar la autenticación con JWT Refresh automático.

---

**Este README será actualizado conforme avance el proyecto.**
