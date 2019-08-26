FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING 'utf-8'
ENV LANG 'en_US.UTF-8'
ENV LANGUAGE=en_US:en
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /code/
WORKDIR /code/

EXPOSE 8000

RUN BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
        gdal-bin \
        wget \
        git \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS

ADD . /code/

RUN wget https://deb.nodesource.com/setup_10.x -O nodesource.sh \
    && bash nodesource.sh \
    && apt install -y nodejs \
    && npm ci
    # && npm run build

RUN set -ex \
    && python3.7 -m venv /venv \
    && /venv/bin/pip install -U pip poetry \
    && /venv/bin/poetry install
