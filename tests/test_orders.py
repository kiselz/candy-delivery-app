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


def test_add_new_order(client):
    """Check new order is added or not"""

    body = {
        'data': [
            {
                'order_id': 1,
                'weight': 0.01,
                'region': 666,
                'delivery_hours': ['00:00-23:59']
            }
        ]
    }

    rv = client.post('/orders',
                     json=body)

    json_data = rv.get_json()
    print(json_data)
    assert len(json_data['orders']) > 0
    assert json_data['orders'][0]['id'] == 1


def test_validation_error(client):
    """Can order be added twice"""

    body = {
        'data': [
            {
                'order_id': 1,
                'weight': 0.01,
                'region': 666,
                'delivery_hours': ['00:00-23:59']
            }
        ]
    }

    rv = client.post('/orders',
                     json=body)
    rv = client.post('/orders',
                     json=body)

    json_data = rv.get_json()
    assert len(json_data['validation_error']) > 0
    assert json_data['validation_error']['orders'][0]['id'] == 1
