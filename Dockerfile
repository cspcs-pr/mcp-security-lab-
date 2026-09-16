# Imagem do MCP Security Lab (uso educacional)
FROM python:3.12-slim

WORKDIR /app

# Instala dependencias primeiro para aproveitar cache de camadas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Roda como usuario nao-root (boa pratica)
RUN useradd --create-home labuser
USER labuser

# Segredos devem ser injetados em runtime, nunca embutidos na imagem
ENV MCP_HMAC_SECRET="" \
    APP_API_KEY=""

CMD ["python", "-m", "pytest", "-q"]
