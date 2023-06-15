FROM amd64/python:3.10-slim

WORKDIR /usr/app

RUN pip install -U pip &&\
    pip install rpyc==5.3.1 kafka-python==2.0.2

COPY client.py client.py
