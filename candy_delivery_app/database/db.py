import sqlite3
from flask import current_app
from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DB_PATH']
        )
    return g.db


def init_db():
    """
    Initialize the database based on the schema.sql file
    """
    db = get_db()
    with current_app.open_resource(
            current_app.config['DB_SCHEMA_PATH']) as file:
        db.executescript(file.read().decode('utf-8'))


def insert(table_name, *args):
    """
    Insert into the table a new row all required properties.
    Length of args should be equal to the column count.
    """

    db = get_db()
    cur = db.execute('SELECT * FROM {}'.format(table_name))
    column_names = [description[0] for description in cur.description]

    cur = db.execute(
        'INSERT INTO {table_name}({column_names}) VALUES({args})'.format(
            table_name=table_name,
            column_names=','.join(column_names),
            args=','.join(map(str, args)),
        ))
    db.commit()
    cur.close()


def get_courier_type_id(courier_type):
    """
    Get courier type id based on courier type
    """
    db = get_db()
    cur = db.execute(
        'SELECT id FROM courier_type WHERE type=?', (courier_type,)
    )
    courier_type_id = cur.fetchone()[0]
    cur.close()
    return courier_type_id


def create_courier(courier):
    """
    Create new courier in the database
    """

    # Create a new row in the 'couriers' table
    # args = (courier_id, courier_type_id, rating, earnings)
    args = (courier['courier_id'],
            get_courier_type_id(courier['courier_type']),
            0.0,
            0,
            )
    insert('courier', *args)

    # Create new rows in the 'couriers_regions' table
    for region in courier['regions']:
        # args = (courier_id, region)
        args = (courier['courier_id'], region,)
        insert('couriers_regions', *args)

    # Create new rows in the 'couriers_working_hours' table
    for working_hour in courier['working_hours']:
        # args = (courier_id, time(work_start), time(work_end))

        work_start, work_end = working_hour.split('-')
        print(work_start, work_end)
        args = (courier['courier_id'],
                '"{}"'.format(work_start),
                '"{}"'.format(work_end),
                )
        insert('couriers_working_hours', *args)
