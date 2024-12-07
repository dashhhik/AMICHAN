ve:
	python3 -m venv .ve; \
	. .ve/bin/activate; \
	pip install -r requirements.txt

docker_build:
	docker-compose up -d --build

docker_build_postgres:
	docker-compose up -d postgres --build

docker_up:
	docker-compose up -d

docker_down:
	docker-compose down

docker_restart:
	docker-compose stop
	docker-compose up -d

docker_logs:
	docker-compose logs --tail=100 -f

migration:
	alembic revision --autogenerate -m "$(message)"

migrate:
	alembic upgrade head