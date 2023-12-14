# Builder
FROM python:3.8.13-slim-buster as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN apt-get update \
    && apt-get install -y gcc netcat curl make git \
    && curl -sSL https://install.python-poetry.org | python3 - && poetry --version

WORKDIR /usr/src/rantools

COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . .

# Runner
FROM python:3.8.13-slim-buster as runner

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/usr/src/rantools

RUN apt-get update \
    && apt-get install -y netcat

RUN mkdir -p ${APP_HOME}/staticfiles
RUN addgroup --system anpusr && adduser --system --group anpusr

COPY --from=builder /usr/src/rantools ${APP_HOME}
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN sed -i 's/\r$//g' ${APP_HOME}/entrypoint.sh
RUN chmod +x ${APP_HOME}/entrypoint.sh

RUN chown -R anpusr:anpusr ${APP_HOME}
USER anpusr
WORKDIR ${APP_HOME}

ENTRYPOINT ["/usr/src/rantools/entrypoint.sh"]