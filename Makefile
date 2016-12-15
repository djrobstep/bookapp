pip:
	pip install -U pip
	pip install -U -r requirements.txt

run_app:
	FLASK_DEBUG=true FLASK_APP=app.py flask run

run_app_prod:
	DB_URL=postgresql:///books_production FLASK_DEBUG=true FLASK_APP=app.py flask run

sync_from_model:
	python migrations.py sync

generate_pending:
	python migrations.py pending

migrate_prod:
	psql -1 -f MIGRATIONS/pending.sql postgresql:///books_production

production_dump:
	pg_dump --inserts --no-owner --no-privileges -f MIGRATIONS/production.dump.sql books_production

deploy_prod: migrate_prod production_dump generate_pending

lint:
	PYFLAKES_NODOCTEST=1 flake8 .

test:
	py.test -x

test_n:
	py.test -x -n=5
