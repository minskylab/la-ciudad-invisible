FROM python:3.8.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN apk --purge del .build-deps


COPY . /usr/src/app/

CMD ["python3", "/usr/src/app/main.py"]