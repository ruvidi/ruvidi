from flask import Blueprint, request, render_template

index_blueprint = Blueprint("index_blueprint", "index_blueprint", url_prefix='/')


@index_blueprint.get('/')
def hello():
    return render_template("index.html")
