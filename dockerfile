FROM python:3.8.2-alpine
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


RUN apk update && apk add bash


COPY requirements.txt app/requirements.txt 
COPY /src /app/src
COPY /test /app/test

WORKDIR ./app

RUN ls -a

# RUN pip install pipenv
# RUN pipenv shell

RUN pip install -r requirements.txt
# RUN pipenv install --system --deploy --ignore-pipfile




ENTRYPOINT ["/bin/bash", "-c", "python3 $0 $@" ]
# ENTRYPOINT ["python3", "src/main.py"]