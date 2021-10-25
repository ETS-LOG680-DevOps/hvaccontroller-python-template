FROM python:3.8.2-alpine
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


RUN apk update && apk add bash


COPY config.sh app/config.sh
COPY requirements.txt app/requirements.txt 
COPY /.env app/.env
COPY /src /app/src
COPY /test /app/test

WORKDIR ./app

RUN ls -a

# RUN pip install pipenv
# RUN pipenv shell

RUN pip install -r requirements.txt
# RUN pipenv install --system --deploy --ignore-pipfile




# ENTRYPOINT ["/bin/bash", "-c", "$@" ]
ENTRYPOINT ["python3", "src/main.py"]