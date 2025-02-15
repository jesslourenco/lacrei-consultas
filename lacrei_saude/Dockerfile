## Stage 1 ##
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y \
  curl \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root

## Stage 2 ##
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  curl \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"] 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

