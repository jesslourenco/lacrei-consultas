FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y \
  curl \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# 🚀 Disable virtual environment creation
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies globally
RUN poetry install --no-interaction --no-root

##### Stage 2: Runtime #####
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
  && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local /usr/local

# Copy application source code
COPY . .

# Expose Django’s default port
EXPOSE 8000

# 🚀 Start Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

