FROM python:3.13-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY openclaw/ ./openclaw/
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["python", "-m", "openclaw.main"]
