#!/bin/bash
set -xe

DIRS="wcc"

FLAKE_CONF="--max-line-length=80"

autoflake \
    --recursive \
    --remove-all-unused-imports \
    --remove-unused-variables \
    --in-place \
    ${DIRS}

black ${DIRS}

isort ${DIRS}

flake8 ${DIRS}  ${FLAKE_CONF}

mypy ${DIRS}
