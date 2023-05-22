#FROM python:3.10-alpine
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#COPY ./requirements.txt /requirements.txt
#RUN apk add --update --no-cache postgresql-client jpeg-dev libffi-dev chromium chromium-chromedriver
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev aws-cli
#RUN export PATH=$PATH:/usr/bin/chromedriver
#RUN pip install --upgrade pip
#
#RUN pip install -r /requirements.txt
#RUN pip install python-telegram-bot==20.0a4
#RUN pip install redis
#RUN apk del .tmp-build-deps
#
#RUN mkdir /app
#COPY . /app
#WORKDIR /app



# Development stage
FROM python:3.9-alpine AS development

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache \
    gcc \
    libc-dev \
    linux-headers \
    postgresql-dev \
    musl-dev \
    zlib-dev \
    libffi-dev \
    jpeg-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-alpine AS production

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache \
    postgresql-client \
    chromium \
    chromium-chromedriver \
    libffi \
    jpeg-dev \
    zlib-dev

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc \
    libc-dev \
    linux-headers \
    postgresql-dev \
    musl-dev \
    zlib-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install python-telegram-bot==20.0a4 && \
    pip install redis && \
    apk del .tmp-build-deps
RUN export PATH=$PATH:/usr/bin/chromedriver
#COPY . /app

# Final base image
FROM production AS final
COPY --from=development /usr/local /usr/local

WORKDIR /app