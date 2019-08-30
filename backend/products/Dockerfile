FROM python:3.7-alpine

WORKDIR /app/src

COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip && pip install -r requirements-dev.txt
