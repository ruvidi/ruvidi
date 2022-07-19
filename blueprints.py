from flask import Blueprint, request

index_blueprint = Blueprint("index_blueprint", url_prefix='/')


@index_blueprint.get('/')
def hello():
    return "Hello, world!"
