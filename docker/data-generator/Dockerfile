FROM amd64/python:3.10-slim

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

RUN pip install -U pip &&\
    pip install scikit-learn==1.2.2 pandas==2.0.1 psycopg2-binary==2.9.6 redis

COPY data_generator.py data_generator.py
