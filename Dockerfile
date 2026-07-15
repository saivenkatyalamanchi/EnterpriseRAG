FROM python:3.13-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-dev --frozen

# Copy application code
COPY . .

# Expose the default FastAPI port
EXPOSE 8000

# Run in production mode, bind to all interfaces
CMD ["uv", "run", "fastapi", "run", "backend/app/main.py", "--host", "0.0.0.0"]