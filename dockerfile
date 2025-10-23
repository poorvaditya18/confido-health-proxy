FROM python:3.11-slim

# keep Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
&& rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src

RUN useradd --create-home appuser \
&& chown -R appuser:appuser /app
USER appuser

WORKDIR /app/src

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]