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


def row_exists(table_name, column_name, column_value):
    """
    Check whether the same row already exist in the table.
    column_name - name of a column with which row will be found
    column_value - value of this column
    """

    return len(get(table_name, column_name, column_value)) != 0


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
            args=','.join(map(lambda x:
                              'NULL' if x is None else '"{}"'.format(x),
                              args)),
        ))
    db.commit()
    cur.close()


def update(table_name, column_name, column_value, **kwargs):
    """
    Update in the table already existed row
    column_name - name of a column with which a row will be found
    column_value - value of this column
    kwargs - properties to update
    """

    db = get_db()
    cur = db.execute(
        'UPDATE {table_name} SET {kwargs} '
        'WHERE {column_name} = {column_value}'.format(
            table_name=table_name,
            kwargs=','.join(['{} = "{}"'.format(key, value)
                             for key, value in kwargs.items()]),
            column_name=column_name,
            column_value=column_value
        )
    )
    db.commit()
    cur.close()


def delete(table_name, column_name, column_value):
    """
    Delete in the table all rows that has column_name equal to unique value
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


def get_courier_type(courier_type_id):
    """
    Get courier type based on courirer_type_id
    """
    return get('courier_type', 'id', courier_type_id)[0]['type']


def get_courier_type_id(courier_type):
    """
    Get courier type id based on courier type
    """
    return get('courier_type', 'type', courier_type)[0]['id']


def get_courier_type_weight(courier_type_id):
    """
    Get courier type weight based on courier type id
    """
    return get('courier_type', 'id', courier_type_id)[0]['weight']


def update_courier(courier):
    """
    Update already existed courier in the database
    """

    # Update the row in the 'courier' table
    # key - property name, value - new value of the property
    properties = {
        'courier_id': courier['courier_id'],
        'courier_type': courier['courier_type'],
    }
    update('courier', 'courier_id', courier['courier_id'], **properties)

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
                work_start,
                work_end,
                )
        insert('couriers_working_hours', *args)


def create_courier(courier):
    """
    Create new courier in the database
    """

    if row_exists('courier', 'courier_id', courier['courier_id']):
        # I guess the server should response validation_error
        # update_courier(courier)
        return False

    # Create a new row in the 'courier' table
    # args = (courier_id, courier_type_id, rating, earnings)
    args = (courier['courier_id'],
            courier['courier_type'],
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
                work_start,
                work_end,
                )
        insert('couriers_working_hours', *args)

    return True


def create_order(order):
    """
    Create new order in the database
    """

    if row_exists('orders', 'order_id', order['order_id']):
        # I guess the server should response validation_error
        return False

    # Create a new row in the 'orders' table
    # args = (order_id, weight, region, is_assigned)
    args = (order['order_id'],
            order['weight'],
            order['region'],
            0,
            )
    insert('orders', *args)

    # Create new rows in the 'orders_delivery_hours' table
    for delivery_hour in set(order['delivery_hours']):
        # args = (order_id, delivery_start, delivery_end)

        delivery_start, delivery_end = delivery_hour.split('-')
        args = (order['order_id'],
                delivery_start,
                delivery_end,
                )
        insert('orders_delivery_hours', *args)

    return True


def get(table_name, column_name, column_value):
    """
    Get row(s) in the table by column name and its value
    :return list
    """

    db = get_db()
    cur = db.execute(
        'SELECT * FROM {table_name} '
        'WHERE {column_name} = "{column_value}"'.format(
            table_name=table_name,
            column_name=column_name,
            column_value=column_value
        )
    )
    rows = cur.fetchall()  # row is just tuple
    cur.close()
    array = []
    if len(rows) >= 1:
        for i in range(len(rows)):
            array.append({})
            for index, column_name in enumerate(cur.description):
                array[i].update({column_name[0]: rows[i][index]})
    return array


def get_order(order_id):
    """
    Get order by order_id
    """

    order = get(
        table_name='orders',
        column_name='order_id',
        column_value=order_id)

    if len(order) != 0:
        delivery_hours = get(
            table_name='orders_delivery_hours',
            column_name='order_id',
            column_value=order[0]['order_id']
        )

        order[0]['delivery_hours'] = []
        for delivery_hour in delivery_hours:
            order[0]['delivery_hours'].append(
                '{}-{}'.format(
                    delivery_hour['delivery_start'],
                    delivery_hour['delivery_end'],
                )
            )
        return order[0]
    else:
        return None


def get_all_unassigned_orders():
    """
    Get all orders with column 'is_assigned' equal to False
    """
    orders = get(
        table_name='orders',
        column_name='is_assigned',
        column_value=0)
    for i in range(len(orders)):
        orders[i] = get_order(orders[i]['order_id'])
    return orders


def get_courier(courier_id):
    """
    Get courier by courier_id
    courier = {
        'courier_id' : ...,
        'courier_type': ...,
        'rating': ...,
        'earnings': ...,
        'regions': [...],
        'working_hours': [...],
    }
    """
    courier = get(
        table_name='courier',
        column_name='courier_id',
        column_value=courier_id)
    if len(courier) != 0:
        working_hours = get(
            table_name='couriers_working_hours',
            column_name='courier_id',
            column_value=courier[0]['courier_id']
        )

        courier[0]['working_hours'] = []
        for working_hour in working_hours:
            courier[0]['working_hours'].append(
                '{}-{}'.format(
                    working_hour['work_start'],
                    working_hour['work_end'],
                )
            )

        courier[0]['regions'] = []
        regions = get(
            table_name='couriers_regions',
            column_name='courier_id',
            column_value=courier[0]['courier_id']
        )
        for region in regions:
            courier[0]['regions'].append(region['region'])

        return courier[0]
    else:
        return None


def get_courier_assigned_time(courier):
    """
    Get courier assigned time from 'couriers_assigned_time' table
    """
    return get(
        table_name='couriers_assigned_time',
        column_name='courier_id',
        column_value=courier['courier_id'])[0]['assigned_time']


def sign_order_to_courier(order, courier, now):
    """
    Add new row in the 'couriers_with_orders' table
    Change 'is_assgned' column in the 'orders' table
    Create new assigned time for courier if it wasn't created
    """

    if not(row_exists(
            table_name='couriers_assigned_time',
            column_name='courier_id',
            column_value=courier['courier_id'])):
        args = (
            courier['courier_id'],
            now,
        )
        insert('couriers_assigned_time', *args)

    assigned_time = get_courier_assigned_time(courier)

    args = (
        courier['courier_id'],
        order['order_id'],
        assigned_time,
        0,
        None,
    )
    insert('couriers_with_orders', *args)

    properties = {
        'is_assigned': 1
    }
    update('orders', 'order_id', order['order_id'], **properties)


def untie_order_from_courier(order, courier):
    """
    Delete row in the 'couriers_with_orders' table
    Change 'is_assigned' column to 0 in the 'orders' table
    """

    delete('couriers_with_orders', 'order_id', order['order_id'])
    properties = {
        'is_assigned': 0
    }
    update('orders', 'order_id', order['order_id'], **properties)


def get_courier_orders(courier):
    """
    Get all orders assigned to the given courier
    :return list
    """

    rows = get('couriers_with_orders', 'courier_id', courier['courier_id'])
    orders = []
    for row in rows:
        if not(row['is_completed']) and \
                row['courier_id'] == courier['courier_id']:
            orders.append(get_order(row['order_id']))
    return orders
