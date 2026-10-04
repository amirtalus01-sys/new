FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY constraints.txt /app/constraints.txt

RUN python -m pip install --upgrade pip \
    && python -m pip install --constraint /app/constraints.txt \
       "https://github.com/M0-AR/agent-reach-mcp/archive/refs/heads/main.zip"

COPY launcher.py /app/launcher.py

EXPOSE 8000

CMD ["python", "/app/launcher.py"]
