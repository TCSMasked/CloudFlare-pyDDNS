FROM python:3.10-slim

WORKDIR /app

COPY src/main.py /app/ddns_updater.py
COPY requirements.txt /app/requirements.txt
COPY config.json /app/config.json
COPY data/db.json /app/data/db.json

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/src/main.py"]