FROM python:3.8.3-alpine as alpine-build
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV HVAC_HOST=http://178.128.234.252:32775
ENV HVAC_TOKEN=WBhinj3isJ

RUN #python -m unittest discover -v

CMD ["python", "./src/main.py"]
