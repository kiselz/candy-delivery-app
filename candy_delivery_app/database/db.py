import sqlite3
from flask import current_app
from flask import g
import os


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DB_PATH']
        )
    return g.db


def init_db():
    db = get_db()
    with current_app.open_resource(
            current_app.config['DB_SCHEMA_PATH']) as file:
        print(os.curdir)
        db.executescript(file.read().decode('utf-8'))
