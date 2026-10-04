FROM node:24-slim AS node_runtime

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Bring in a current Node/npm runtime required by mcporter.
COPY --from=node_runtime /usr/local/ /usr/local/

# Server-safe Agent Reach dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl git gh ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Exa semantic search backend.
RUN npm install -g mcporter \
    && mcporter config add exa https://mcp.exa.ai/mcp --scope home

COPY constraints.txt /app/constraints.txt

RUN python -m pip install --upgrade pip \
    && python -m pip install --constraint /app/constraints.txt \
       "https://github.com/M0-AR/agent-reach-mcp/archive/refs/heads/main.zip" \
       "yt-dlp[default]>=2026.7.4" \
       "bilibili-cli" \
       "yfinance>=1.4.1"

COPY launcher.py /app/launcher.py

EXPOSE 8000

CMD ["python", "/app/launcher.py"]
