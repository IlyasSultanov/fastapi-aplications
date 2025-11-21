FROM python:3.12.6-bookworm

# --- System settings ---
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# --- Install uv and deps ---
RUN pip install --upgrade pip wheel "uv"

# Use uv instead of pip/poetry
RUN uv config virtualenvs.create false

# Copy project configuration
COPY pyproject.toml poetry.lock ./

# Install dependencies (with dev deps for pytest)
RUN uv sync --dev

# Copy all source code
COPY . .

# Make scripts executable
RUN chmod +x prestart.sh
RUN chmod +x run

# --- Run app ---
ENTRYPOINT ["./prestart.sh"]
CMD ["./run"]
