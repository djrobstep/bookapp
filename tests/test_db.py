from migrations import load_post_migration, load_from_app
from sqlbag import temporary_database as temporary_db
from sqlbag import S
from migra import Migration


def test_db():
    with temporary_db() as CURRENT_DB_URL, temporary_db() as TARGET_DB_URL:
        load_post_migration(CURRENT_DB_URL)
        load_from_app(TARGET_DB_URL)

        with S(CURRENT_DB_URL) as s_current, S(TARGET_DB_URL) as s_target:
            m = Migration(s_current, s_target)
            m.set_safety(False)
            m.add_all_changes()
            assert not m.statements
