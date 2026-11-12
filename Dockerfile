FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HP_HOST=0.0.0.0 \
    HP_PORT=2222

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser ssh_honeypot.py .
USER appuser

EXPOSE 2222
CMD ["python", "ssh_honeypot.py"]
