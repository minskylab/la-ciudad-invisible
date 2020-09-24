FROM python:3.8.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache build-base gcc musl-dev postgresql-dev
RUN apk add linux-headers
# --virtual .build-deps

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# RUN apk --purge del .build-deps

COPY . /usr/src/app/

ENV PROD=true
ENV TZ="America/Lima"

CMD ["python3", "/usr/src/app/main.py"]