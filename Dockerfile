FROM ubuntu:20.04

WORKDIR /app


ARG DEBIAN_FRONTEND=noninteractive

COPY . /app

RUN apt-get update && apt-get install -y python3 python3-pip tzdata sqlite3
RUN pip3 install --no-cache-dir -r requirements.txt
ENV DJANGO_SETTINGS_MODULE=apps.settings

