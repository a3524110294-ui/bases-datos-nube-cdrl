.PHONY: setup verify run

setup:
	@mkdir -p artifacts evidence docs db/migrations db/seed src tests
	@test -f .env.example
	pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt
	docker compose up -d postgres

verify:
	@bash scripts/verify_base.sh
	python src/apply_migrations.py
	python db/seed/seed_data.py
	python -m pytest tests/ -v

run:
	docker compose up