from .server.app import create_app
from .server.app import register_blueprints
from .database.db import init_db


app = create_app()
with app.app_context():
    init_db()

register_blueprints(app)
app.run('0.0.0.0', 5000)
