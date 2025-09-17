# Multi-stage build for the MCP Docassemble server

FROM python:3.12-slim AS builder

WORKDIR /build

ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --upgrade pip build && \
    python -m build --wheel --outdir /dist

FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/mcp/.local/bin:$PATH"

RUN groupadd --system mcp && useradd --system --gid mcp --create-home mcp

WORKDIR /home/mcp

COPY --from=builder /dist /dist
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir /dist/*.whl

COPY .env.example ./

USER mcp

ENV DOCASSEMBLE_BASE_URL="" \
    DOCASSEMBLE_API_KEY=""

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import os,sys; sys.exit(0 if os.getenv('DOCASSEMBLE_BASE_URL') and os.getenv('DOCASSEMBLE_API_KEY') else 1)"

ENTRYPOINT ["mcp-docassemble"]
CMD ["serve"]
