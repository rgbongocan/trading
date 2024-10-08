# derived from https://github.com/orgs/python-poetry/discussions/1879#discussioncomment-216865
FROM python:3.11-slim as python-base

ENV PYTHONBUFFERED=1 \
    # don't write *.pyc
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1\
    POETRY_HOME="/opt/poetry"\
    # create poetry virtualenv in project root
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # requirements and virtualenv go here
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# build deps, create virtualenv
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential binutils libgdal-dev gdal-bin

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install runtime deps
RUN poetry install --only main

FROM python-base as development
WORKDIR $PYSETUP_PATH

# copy built poetry and virtualenv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install

WORKDIR /app
COPY . .

EXPOSE 8000
CMD ["python", "/api/manage.py", "runserver", "0.0.0.0:8000"]
