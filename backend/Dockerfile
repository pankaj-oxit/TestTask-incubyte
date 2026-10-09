FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

RUN pip install --no-cache-dir "setuptools>=68" wheel \
    && pip install --no-cache-dir -e .

COPY scripts ./scripts
RUN chmod +x scripts/railway-start.sh scripts/docker-entrypoint.sh

EXPOSE 8000

# Railway / production: migrate then listen on $PORT (no --reload)
CMD ["/bin/sh", "/app/scripts/railway-start.sh"]
