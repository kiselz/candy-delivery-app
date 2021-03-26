from .server.app import app
from .database.db import init_db

with app.app_context():
    init_db()
app.run('0.0.0.0', 5000)
