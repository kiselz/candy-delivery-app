import pytest
from candy_delivery_app.server.app import create_app
from candy_delivery_app.server.app import register_blueprints
from candy_delivery_app.server.configurations import TestConfig
from candy_delivery_app.database.db import init_db


@pytest.fixture
def client():
    app = create_app(TestConfig)
    register_blueprints(app)

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_add_new_courier(client):
    """Check new courier is added or not"""

    body = {
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:05", "09:00-11:00"],
            }
        ]
    }

    rv = client.post('/couriers',
                     json=body)

    json_data = rv.get_json()
    assert len(json_data['couriers']) > 0
    assert json_data['couriers'][0]['id'] == 1


def test_validation_error(client):
    """Can courier be added twice"""

    body = {
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:05", "09:00-11:00"],
            }
        ]
    }

    rv = client.post('/couriers',
                     json=body)
    rv = client.post('/couriers',
                     json=body)

    json_data = rv.get_json()
    assert len(json_data['validation_error']) > 0
    assert json_data['validation_error']['couriers'][0]['id'] == 1


def test_patch_courier(client):
    """Courier's change"""

    body = {
        'data': [
            {
                'courier_id': 1,
                'courier_type': 'foot',
                'regions': [1, 12, 22],
                'working_hours': ["11:35-14:05", "09:00-11:00"],
            }
        ]
    }

    rv = client.post('/couriers',
                     json=body)

    body = {
        'courier_type': 'car',
        'regions': [666],
        'working_hours': ["10:00-15:00"],
        'courier_id': 666,
    }

    rv = client.patch('/couriers/1',
                      json=body)

    json_data = rv.get_json()
    assert json_data['courier_type'] == 'car'
    assert json_data['regions'] == [666]
    assert json_data['working_hours'] == ["10:00-15:00"]

