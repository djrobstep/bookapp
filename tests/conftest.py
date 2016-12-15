import pytest
import io
from sqlbag import temporary_database

from bookapp import get_app

from migrations import load_pre_migration, load_post_migration

with io.open('MIGRATIONS/pending.sql') as f:
    pending_contents = f.read()


if pending_contents.strip():
    DATABASE_SETUPS_TO_TEST = [
        load_pre_migration,
        load_post_migration
    ]
else:
    DATABASE_SETUPS_TO_TEST = [
        load_post_migration
    ]


@pytest.fixture(params=DATABASE_SETUPS_TO_TEST)
def db(request):
    with temporary_database() as test_db_url:
        setup_method = request.param
        setup_method(test_db_url)
        yield test_db_url


@pytest.fixture()
def client(db):
    app = get_app(db)
    with app.test_client() as c:
        yield c
