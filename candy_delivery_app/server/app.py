from flask import Flask
from .configurations import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
