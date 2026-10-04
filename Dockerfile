FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

# Core Agent Reach runtime dependencies for server-safe channels.
# These match the upstream Panniantong/Agent-Reach install guidance:
# GitHub CLI, Node/npm for mcporter, ffmpeg for transcription, and git for pinned CLI installs.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl git gh nodejs npm ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Exa semantic search backend (no API key required by Agent Reach's current route).
RUN npm install -g mcporter \
    && mcporter config add exa https://mcp.exa.ai/mcp --scope home

COPY constraints.txt /app/constraints.txt

# MCP-capable fork is based directly on Panniantong/Agent-Reach v1.5.0 and
# adds the hosted MCP interface needed by ChatGPT. Install the server-safe
# zero-config backends alongside it.
RUN python -m pip install --upgrade pip \
    && python -m pip install --constraint /app/constraints.txt \
       "https://github.com/M0-AR/agent-reach-mcp/archive/refs/heads/main.zip" \
       "yt-dlp[default]>=2026.7.4" \
       "bilibili-cli" \
       "yfinance>=1.4.1"

COPY launcher.py /app/launcher.py

EXPOSE 8000

CMD ["python", "/app/launcher.py"]
