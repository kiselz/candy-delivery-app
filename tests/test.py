from candy_delivery_app.server.app import create_app
from candy_delivery_app.server.configurations import TestConfig


app = create_app(TestConfig)
