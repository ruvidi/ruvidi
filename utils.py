from uuid import uuid4
import json


def generate_secret_key(app):
    app.secret_key = uuid4().hex
    return app


def load_configuration(app):
    app.config.from_file("configuration.json", json.load)
    return app
