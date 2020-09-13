FROM python:3.8.5

RUN pip install --upgrade --no-cache-dir pip \
 && pip install --no-cache-dir poetry

WORKDIR /srv

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false \
 && poetry install \
 && rm pyproject.toml poetry.lock
