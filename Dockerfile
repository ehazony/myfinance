FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev libffi-dev chromium chromium-chromedriver
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN export PATH=$PATH:/usr/bin/chromedriver
RUN pip install --upgrade pip

RUN pip install -r /requirements.txt
RUN pip install python-telegram-bot==20.0a4
RUN pip install redis
RUN apk del .tmp-build-deps

RUN mkdir /app
COPY . /app
WORKDIR /app

