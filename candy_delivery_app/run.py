import argparse
from .server.app import create_app
from .server.app import register_blueprints
from .database.db import init_db
from .server.configurations import DevConfig
from .server.configurations import ProdConfig
from .server.configurations import TestConfig
from waitress import serve


HOST = '0.0.0.0'
PORT = 5000

parser = argparse.ArgumentParser(
    description='Run server in different configurations'
)
configuration = parser.add_mutually_exclusive_group(required=True)
configuration.add_argument('--dev',
                           help='Development configuration',
                           action='store_true')
configuration.add_argument('--test',
                           help='Test configuration',
                           action='store_true')
configuration.add_argument('--prod',
                           help='Production configuration',
                           action='store_true')

args = parser.parse_args()

app = None
if args.dev:
    app = create_app(DevConfig)
elif args.test:
    app = create_app(TestConfig)
elif args.prod:
    app = create_app(ProdConfig)

with app.app_context():
    init_db()

register_blueprints(app)

if args.prod:
    serve(app, host=HOST, port=PORT)
else:
    app.run(host=HOST, port=PORT)
