import sys
import io

from migra import Migration
from sqlbag import S, temporary_database as temporary_db, \
    load_sql_from_folder, load_sql_from_file

from config import DB_URL

from bookapp.models import Model


def prompt(question):
    print(question + ' ', end='')
    return input().strip().lower() == 'y'


def load_pre_migration(dburl):
    with S(dburl) as s:
        load_sql_from_file(s, 'MIGRATIONS/production.dump.sql')


def load_post_migration(dburl):
    with S(dburl) as s:
        load_sql_from_file(s, 'MIGRATIONS/production.dump.sql')

    with S(dburl) as s:
        load_sql_from_file(s, 'MIGRATIONS/pending.sql')


def load_from_app(dburl):
    with S(dburl) as s:
        Model.metadata.create_all(s.bind.engine)
        load_sql_from_folder(s, 'bookapp/SQL')


def sync():
    with temporary_db() as TEMP_DB_URL:
        with S(TEMP_DB_URL) as s_target:
            Model.metadata.create_all(s_target.bind.engine)
            load_sql_from_folder(s_target, 'bookapp/SQL')

        with S(DB_URL) as s_current, S(TEMP_DB_URL) as s_target:
            m = Migration(s_current, s_target)
            m.set_safety(False)
            m.add_all_changes()

            if m.statements:
                print('THE FOLLOWING CHANGES ARE PENDING:', end='\n\n')
                print(m.sql)

                if prompt('Apply these changes?'):
                    print('Applying...')
                    m.apply()
                else:
                    print('Not applying.')
            else:
                print('Already synced.')


def pending():
    with temporary_db() as CURRENT_DB_URL, temporary_db() as TARGET_DB_URL:
        load_pre_migration(CURRENT_DB_URL)
        load_from_app(TARGET_DB_URL)

        with S(CURRENT_DB_URL) as s_current, S(TARGET_DB_URL) as s_target:
            m = Migration(s_current, s_target)

            m.set_safety(False)
            m.add_all_changes()

            print('Pending:\n{}'.format(m.sql))

            with io.open('MIGRATIONS/pending.sql', 'w') as w:
                w.write(m.sql)


if __name__ == '__main__':
    try:
        task_method = getattr(sys.modules[__name__], sys.argv[1])
    except AttributeError:
        print('no such task')

    task_method(*sys.argv[2:])
