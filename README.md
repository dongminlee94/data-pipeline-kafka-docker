# Data Pipeline Kafka Docker

## Prerequisites

- Install [Docker](https://docs.docker.com/engine/install/).

## Preparation

Install Python 3.10 on [Pyenv](https://github.com/pyenv/pyenv#installation) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html) and execute the following commands:

```bash
$ make init     # setup packages (need only once)
```

## How To Play

### 1. Create Infra

```bash
$ make compose          # create all the containers
```

You can delete the containers.

```bash
$ make compose-clean    # delete the containers
```

You can divide the containers and create them.

```bash
$ make db       # create a postgres (source DB), a minio (target DB), a data generator, and a bucket creator (need only once)
$ make kafka    # create a kafka cluster (need only once)
$ make glue     # create a glue process that automated ETL (need only once)
```

You can delete the divided containers.

```bash
$ make glue-clean   # delete the glue process
$ make kafka-clean  # delete the kafka cluster
$ make db-clean     # delete the databases and the rest.
```

### 2. TBD

## For Developers

```bash
$ make check          # all static analysis scripts
$ make format         # format scripts
$ make lint           # lints scripts
```
