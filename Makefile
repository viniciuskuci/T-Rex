.PHONY: build compose down

build: 
	docker build -t python:3.10-slim -f docker/Dockerfile .
compose:
	docker compose -f compose/docker-compose.yml up -d
down:
	docker compose -f compose/docker-compose.yml down
