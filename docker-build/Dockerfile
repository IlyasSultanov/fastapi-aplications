FROM python:3.12.6-slim

# --- System settings ---
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# --- Install uv (correctly) ---
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Now you can use uv reliably
RUN uv --version

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies (dev included)
RUN uv sync --all-extras --dev

# Copy source
COPY . .

# Make scripts executable
RUN chmod +x prestart.sh

# --- Run app ---
ENTRYPOINT ["./prestart.sh"]
CMD ["uv", "run", "uvicorn", "app.main:main_app", "--host", "0.0.0.0", "--port", "8000"]