FROM python:3.11.2
WORKDIR /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV HVAC_HOST=$HVAC_HOST
ENV HVAC_TOKEN=$HVAC_TOKEN
CMD ["python", "main.py"]