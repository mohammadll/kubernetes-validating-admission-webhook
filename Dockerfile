FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY validate.py .

COPY wsgi.py .

CMD gunicorn --certfile=/certs/webhook.crt --keyfile=/certs/webhook.key --bind 0.0.0.0:443 wsgi:webhook
