from flask import Flask
from flask_migrate import Migrate
from flask_minify import Minify

from database import database
from redis_queue import redis_queue
from utils import (
    generate_secret_key,
    load_configuration
)
from blueprints import (
    index_blueprint,
    upload_blueprint,
    comment_blueprint
)

app = Flask(__name__, "/static")
minify = Minify(app, html=True, js=True, cssless=True)

generate_secret_key(app)
load_configuration(app)

database.init_app(app)
migrate = Migrate(app, database)

redis_queue.init_app(app)

app.register_blueprint(index_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(comment_blueprint)
