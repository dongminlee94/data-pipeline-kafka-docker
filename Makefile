# ========================================================================================
# ======================================== Basics ========================================
# ========================================================================================
install-poetry:
	@echo "Install poetry";\
	curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2

init:
	@echo "Construct development environment";\
	if [ -z $(VIRTUAL_ENV) ]; then echo Warning, Virtual Environment is required; fi;\
	if [ -z `command -v poetry` ];\
		then make install-poetry;\
	fi;\
	pip install -U pip
	poetry install
	poetry run pre-commit install

check: format lint

format:
	poetry run black .

lint:
	poetry run pyright
	poetry run ruff docker --fix

# ==========================================================================================
# ======================================== Database ========================================
# ==========================================================================================
database:
	docker compose -p database -f docker-compose-database.yaml up -d

database-clean:
	docker compose -p database down -v
	docker rmi database-data-generator

# =======================================================================================
# ======================================== Kafka ========================================
# =======================================================================================
kafka:
	docker compose -p kafka -f docker-compose-kafka.yaml up -d

kafka-clean:
	docker compose -p kafka down -v
	docker rmi kafka-connect

source-postgres:
	curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @config/source_postgres.json

source-postgres-clean:
	curl -X DELETE "http://localhost:8083/connectors/{source-postgres}"

sink-postgres:
	curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d @config/sink_postgres.json

sink-postgres-clean:
	curl -X DELETE "http://localhost:8083/connectors/{sink-postgres}"
