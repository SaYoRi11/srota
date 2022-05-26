# syntax=docker/dockerfile:1

# FROM python:3.8-slim-buster
# WORKDIR /app/api
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# CMD uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000

FROM python:3.8-slim-buster as base

FROM base as builder
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM base as runtime
COPY --from=builder /opt/venv /opt/venv
COPY . .
ENV PATH="/opt/venv/bin:$PATH"
CMD uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8000

