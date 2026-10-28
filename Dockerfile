FROM python:3.10-slim

WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y los modelos
COPY src/ ./src/
COPY models/ ./models/

# Exponer el puerto de la API
EXPOSE 8000

# Encender la válvula del servidor al iniciar el contenedor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
