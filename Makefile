######################
#   initialization   #
######################
init:
	pip install -U pip
	pip install pdm
	pdm install
	pdm run pre-commit install

#######################
#   static analysis   #
#######################
check: format lint

format:
	pdm run black .

lint:
	pdm run mypy docker
	pdm run ruff docker --fix

######################
#   docker compose   #
######################
compose:
	make db
	make kafka
	sleep 60
	make connectors
	make glue

compose-clean:
	make glue-clean
	make kafka-clean
	make db-clean

db:
	docker compose -p db -f docker-compose-db.yaml up -d

db-clean:
	docker compose -p db down -v
	docker rmi db-data-generator

kafka:
	docker compose -p kafka -f docker-compose-kafka.yaml up -d

kafka-clean:
	docker compose -p kafka down -v
	docker rmi kafka-connect

glue:
	docker compose -p glue -f docker-compose-glue.yaml up -d

glue-clean:
	docker compose -p glue down -v
	docker rmi glue-glue-server glue-glue-client

#######################
#   kafka connector   #
#######################
connectors:
	make source-postgres
	make sink-s3

connectors-clean:
	make sink-s3-clean
	make source-postgres-clean

source-postgres:
	curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @config/source_postgres.json

source-postgres-clean:
	curl -X DELETE "http://localhost:8083/connectors/{source-postgres}"

sink-s3:
	curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @config/sink_s3.json

sink-s3-clean:
	curl -X DELETE "http://localhost:8083/connectors/{sink-s3}"
