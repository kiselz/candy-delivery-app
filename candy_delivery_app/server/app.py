from flask import Flask
from .configurations import DevConfig
from ..server import couriers
from ..server import orders


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def register_blueprints(app):
    """Register Flask blueprints"""

    app.register_blueprint(couriers.views.blueprint)
    app.register_blueprint(orders.views.blueprint)
