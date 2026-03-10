.PHONY: run test lint format docker-up docker-down audit

run:
	python -m openclaw.main

test:
	pytest tests/ -v

lint:
	ruff check openclaw/ tests/

format:
	ruff format openclaw/ tests/

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

audit:
	pip-audit -r requirements.txt
