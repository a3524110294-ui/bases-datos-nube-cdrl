.PHONY: setup verify run

setup:
	@mkdir -p artifacts evidence docs db/migrations db/seed src tests
	@test -f .env.example
	pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt
	docker compose up -d postgres

verify:
	@bash scripts/verify_base.sh
	@echo "Esperando a que Postgres este listo..."
	@i=0; until docker compose exec -T postgres pg_isready -U cdrl_dev -d cdrl >/dev/null 2>&1 || [ $$i -ge 30 ]; do i=$$((i+1)); sleep 1; done
	python src/apply_migrations.py
	python db/seed/seed_data.py
	python -m pytest tests/ -v
	python scripts/write_artifact.py

run:
	docker compose up -d postgres
	python scripts/run_summary.py
