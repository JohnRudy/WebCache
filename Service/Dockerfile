FROM python:3.10.14-slim-bookworm

USER root

LABEL maintainer="thejohnrudy@gmail.com"

WORKDIR /app

ENV POETRY_HOME=/opt/poetry
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# for ARM processors we need to fetch some packages separately
RUN apt-get update && \
    apt-get install gcc libc-dev -y && \
    apt-get install --no-install-recommends -y sudo && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge --auto-remove && \
    apt-get clean

RUN python -c 'import urllib.request; print(urllib.request.urlopen("https://install.python-poetry.org").read().decode("utf-8"))' | python && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock /app/

RUN poetry --version && \
    poetry install && \
    rm -rf /root/.cache && \
    rm -rf /var/cache/debconf && \
    find / -regex '^.*\(__pycache__\|\.py[co]\)$' -delete

COPY ./ /app

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8888", "app.asgi:app"]
