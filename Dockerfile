# Usa la imagen oficial de Python como base
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que corre Django
EXPOSE 8000

# Define el comando por defecto para ejecutar el servidor
CMD ["gunicorn", "cheaf_test_tecnico.wsgi:application", "--bind", "0.0.0.0:8000"]