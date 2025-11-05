# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for building packages and MariaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    libmariadb-dev-compat \
    libmariadb-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Disable Poetry venv creation and install dependencies globally
COPY pyproject.toml poetry.lock* README.md /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

# Copy the application code
COPY . .

# Ensure Python outputs logs immediately
ENV PYTHONUNBUFFERED=1

# Default command (overridden in docker-compose)
CMD ["bash"]
