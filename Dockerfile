FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# LA MAGIE EST ICI : On installe le requirements.txt D'ORIGINE + Les paquets pour TON Dashboard Web !
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt && \
    pip install --no-cache-dir --break-system-packages fastapi uvicorn jinja2 python-multipart

COPY . .

EXPOSE 8000

# Démarrage
CMD ["python3", "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]
