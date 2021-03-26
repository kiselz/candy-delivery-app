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


def row_exists(table_name, unique_name, unique_value):
    """
    Check whether the same row already exist in the table.
    unique_name - name of an unique column
    unique_value - value of an unique column
    """

    db = get_db()
    cur = db.execute('SELECT * FROM {} WHERE {} = {}'.format(
        table_name, unique_name, unique_value
    ))
    data = cur.fetchall()
    if len(data) == 0:
        return False
    return True


def insert(table_name, *args):
    """
    Insert into the table a new row with all required properties.
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


def update(table_name, unique_name, unique_value, **kwargs):
    """
    Update in the table already existed row
    unique_name - name of an unique column
    unique_value - value of an unique column
    kwargs - properties to update
    """

    db = get_db()
    cur = db.execute(
        'UPDATE {table_name} SET {kwargs} '
        'WHERE {unique_name} = {unique_value}'.format(
            table_name=table_name,
            kwargs=','.join(['{} = {}'.format(key, value)
                             for key, value in kwargs.items()]),
            unique_name=unique_name,
            unique_value=unique_value
        )
    )
    db.commit()
    cur.close()


def delete(table_name, column_name, column_value):
    """
    Delete in the table all rows that has unique_name equal to unique value
    column_name - name of an unique column
    column_value - value of an unique column
    """

    db = get_db()
    cur = db.execute(
        'DELETE FROM {table_name} WHERE {column_name} = {column_value}'.format(
            table_name=table_name,
            column_name=column_name,
            column_value=column_value,
        )
    )
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


def update_courier(courier):
    """
    Update already existed courier in the database
    """

    # Update the row in the 'courier' table
    # key - property name, value - new value of the property
    properties = {
        'id': courier['courier_id'],
        'courier_type_id': get_courier_type_id(courier['courier_type']),
    }
    update('courier', 'id', courier['courier_id'], **properties)

    # Delete all rows in the 'couriers_regions' table with courier_id
    delete('couriers_regions', 'courier_id', courier['courier_id'])

    # Create new rows in the 'couriers_regions' table
    for region in set(courier['regions']):
        # args = (courier_id, region)
        args = (courier['courier_id'], region,)
        insert('couriers_regions', *args)

    # Delete all rows in the 'couriers_working_hours' table with courier_id
    delete('couriers_working_hours', 'courier_id', courier['courier_id'])

    # Create new rows in the 'couriers_working_hours' table
    for working_hour in set(courier['working_hours']):
        # args = (courier_id, time(work_start), time(work_end))

        work_start, work_end = working_hour.split('-')
        args = (courier['courier_id'],
                '"{}"'.format(work_start),
                '"{}"'.format(work_end),
                )
        insert('couriers_working_hours', *args)


def create_courier(courier):
    """
    Create new courier in the database
    """

    if row_exists('courier', 'id', courier['courier_id']):
        update_courier(courier)
        return

    # Create a new row in the 'courier' table
    # args = (courier_id, courier_type_id, rating, earnings)
    args = (courier['courier_id'],
            get_courier_type_id(courier['courier_type']),
            0.0,
            0,
            )
    insert('courier', *args)

    # Create new rows in the 'couriers_regions' table
    for region in set(courier['regions']):
        # args = (courier_id, region)
        args = (courier['courier_id'], region,)
        insert('couriers_regions', *args)

    # Create new rows in the 'couriers_working_hours' table
    for working_hour in set(courier['working_hours']):
        # args = (courier_id, time(work_start), time(work_end))

        work_start, work_end = working_hour.split('-')
        args = (courier['courier_id'],
                '"{}"'.format(work_start),
                '"{}"'.format(work_end),
                )
        insert('couriers_working_hours', *args)
