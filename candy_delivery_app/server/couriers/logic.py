"""Functions that deal with couriers logic"""
from candy_delivery_app.database.db import get_courier_type_id
from candy_delivery_app.database.db import get_courier_type


def to_courier_row(courier):
    """
    Add to the given courier keys that has courier in the 'courier table'
    ('id' and 'courier_type_id') and delete 'courier_id' and 'courier_type'
    """
    courier.update({
        'id': courier['courier_id'],
        'courier_type_id': get_courier_type_id(courier['courier_type'])
    })
    del courier['courier_id'], courier['courier_type']
    return courier


def to_courier_request(courier):
    """
    Reverse to 'to_couier_row' function.
    Doesn't include rating and earnings keys if they are 0.
    """
    courier.update({
        'courier_id': courier['id'],
        'courier_type': get_courier_type(courier['courier_type_id'])
    })
    del courier['id'], courier['courier_type_id']

    if courier['rating'] == 0:
        del courier['rating']

    if courier['earnings'] == 0:
        del courier['earnings']

    return courier
