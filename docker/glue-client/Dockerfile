FROM amd64/python:3.10-slim

WORKDIR /usr/app

RUN pip install -U pip &&\
    pip install rpyc==5.3.1 confluent-kafka==2.1.1 requests==2.31.0 fastavro==1.7.4

COPY src src
