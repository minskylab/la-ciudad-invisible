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
# --virtual .build-deps

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# RUN apk --purge del .build-deps

COPY . /usr/src/app/

CMD ["python3", "/usr/src/app/main.py"]