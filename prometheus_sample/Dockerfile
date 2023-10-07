FROM python:3.9.1-slim AS base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY main.py main.py

CMD ["python", "main.py"]
