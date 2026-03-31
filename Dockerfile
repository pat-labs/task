# Stage 1: Build and Test
FROM python:3.9-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Ensure path is set for tests to find installed packages
ENV PATH=/root/.local/bin:$PATH

# Copy source code and tests
COPY src ./src
COPY resource ./resource
COPY test ./test

# Run tests
RUN python -m unittest discover -s test

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application source code
COPY src ./src
COPY main.py .
COPY .env .

# Set the entrypoint
CMD ["python", "main.py"]
