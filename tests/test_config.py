from candy_delivery_app.server.app import create_app
from candy_delivery_app.server.configurations import DevConfig
from candy_delivery_app.server.configurations import ProdConfig


def test_production_config():
    """Production config"""
    app = create_app(ProdConfig)
    assert app.config['ENV'] == 'production'
    assert not app.config['DEBUG']


def test_dev_config():
    """Development config"""
    app = create_app(DevConfig)
    assert app.config['ENV'] == 'development'
    assert app.config['DEBUG']
