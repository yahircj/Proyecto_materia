FROM python:3.13-alpine

WORKDIR /api

# Instalar dependencias del sistema
RUN apk add --no-cache mariadb-dev gcc

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto en el que se ejecutará la API
EXPOSE 5000

# Comando para ejecutar la API
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0","--port", "5000"]