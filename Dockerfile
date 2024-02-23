FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN export POETRY_HOME=/opt/poetry \
  && curl -sSL https://install.python-poetry.org | python - --version 1.6.1 \
  && $POETRY_HOME/bin/poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --upgrade pip setuptools \
  && pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location --user -r requirements.txt

COPY ui .
EXPOSE 8500

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python", "-m", "streamlit", "run", "home.py", "--server.port=8500", "--server.address=0.0.0.0"]