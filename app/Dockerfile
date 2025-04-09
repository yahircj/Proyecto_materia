FROM python:3.13-alpine

WORKDIR /app
# Instalar dependencias del sistema
RUN apk add --no-cache mariadb-dev gcc

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la API
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]