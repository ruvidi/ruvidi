from flask import Flask
from flask_migrate import Migrate
from database import database
from utils import (
    generate_secret_key,
    load_configuration
)
from blueprints import index_blueprint

app = Flask(__name__)

generate_secret_key(app)
load_configuration(app)

database.init_app(app)
migrate = Migrate(app, database)

app.register_blueprint(index_blueprint)
