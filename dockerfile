FROM python:3.8.2-alpine


# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV HVAC_HOST=https://log680.vincentboivin.ca
ENV HVAC_TOKEN=89103df59ad0cda23c2f


RUN apk update && apk add bash


COPY requirements.txt app/requirements.txt
COPY /src /app/src
COPY /test /app/test

WORKDIR ./app

RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "$0 $@" ]
