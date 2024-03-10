FROM python:3.11-buster as builder

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./

ENV SECRET_KEY = $SECRET_KEY

ENV POSTGRES_DB = $POSTGRES_DB

ENV POSTGRES_USER = $POSTGRES_USER

ENV POSTGRES_PASSWORD = $POSTGRES_PASSWORD

ENV POSTGRES_HOST = $POSTGRES_HOST

ENV POSTGRES_PORT = $POSTGRES_PORT

RUN pip install django_stubs_ext

RUN python manage.py collectstatic

ENTRYPOINT ["uvicorn", "api.asgi:application", "--host", "0.0.0.0"]
