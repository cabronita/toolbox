FROM python:3.12.13-alpine3.23

ENV TZ='Europe/London'

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY buffer.py ./
COPY simrail ./simrail

ENTRYPOINT ["python", "buffer.py"]
