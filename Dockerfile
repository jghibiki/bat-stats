# Default to the latest slim version of Python
ARG PYTHON_IMAGE_TAG=3.10-slim

###############################################################################
# POETRY BASE IMAGE - Provides environment variables for poetry
###############################################################################
FROM python:${PYTHON_IMAGE_TAG} AS python-poetry-base
# Default to the latest version of Poetry

# Default to the latest version of Poetry
ARG POETRY_VERSION=""

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1


ENV PATH="$POETRY_HOME/bin:$PATH"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

###############################################################################
# POETRY BUILDER IMAGE - Installs Poetry and dependencies
###############################################################################
FROM python-poetry-base AS python-poetry-builder
RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl netcat-traditional
# Install Poetry via the official installer: https://python-poetry.org/docs/master/#installing-with-the-official-installer
# This script respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

###############################################################################
# POETRY RUNTIME IMAGE - Copies the poetry installation into a smaller image
###############################################################################
FROM python-poetry-base AS python-poetry
COPY --from=python-poetry-builder $POETRY_HOME $POETRY_HOME

RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes netcat-traditional

COPY src/ /app/src/
COPY pyproject.toml /app
COPY scripts/entrypoint.sh /app
WORKDIR /app
RUN poetry cache clear --all .
RUN poetry config installer.max-workers 1
RUN poetry run pip install wheel setuptools pip --upgrade
RUN poetry install
WORKDIR /app/src

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]