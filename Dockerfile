# --- Stage 1: Base & Dependencies ---
FROM python:3.9-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install dev tools for linting, static analysis, and testing
RUN pip install black isort flake8

# --- Stage 2: Code Copy ---
# This stage copies the application code once for subsequent analysis and testing stages.
FROM base AS code-copy
WORKDIR /app
COPY src ./src
COPY test ./test
COPY main.py .
COPY .env .
COPY resource ./resource

# --- Stage 3: Formatting Check (isort & black) and Static Analysis (flake8) ---
FROM code-copy AS static-analysis
# Use python -m for better reliability in invoking installed modules
RUN python -m isort --check-only src test
RUN python -m black --check src test
RUN python -m flake8 src test

# --- Stage 4: Unit Tests ---
FROM static-analysis AS tester
RUN python -m unittest discover -s test

# --- Stage 5: Final Runtime ---
FROM python:3.9-slim AS runtime
WORKDIR /app
# Copy only the necessary runtime dependencies from the base stage
COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# Copy only the application code from the code-copy stage
COPY --from=code-copy /app/src ./src
COPY --from=code-copy /app/main.py .
COPY --from=code-copy /app/.env .
COPY --from=code-copy /app/resource ./resource

CMD ["python", "main.py"]