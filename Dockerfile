FROM python:3.11-alpine

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
ENTRYPOINT ["python", "dns_updater.py"]
