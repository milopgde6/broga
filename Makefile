.PHONY: run seed migrate test backup backup-weekly

run:
	python -m app.bot.main

seed:
	python scripts/seed.py

migrate:
	python scripts/migrate.py

test:
	pytest -q

backup:
	bash scripts/backup.sh daily

backup-weekly:
	bash scripts/backup.sh weekly