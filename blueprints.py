from flask import abort, request, Blueprint, render_template
from database import database
from models import Video

index_blueprint = Blueprint("index_blueprint", "index_blueprint", url_prefix='/')


@index_blueprint.get('/')
def index():
    return render_template("index.html")


@index_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not 'title' and 'description' in request.form or not 'video' in request.files:
            return abort(400)
        
        video = Video(request.form['title'], request.form['description'])

        database.session.add(video)
        database.session.commit()

        return render_template("upload_status.html", video=video)
    return render_template("upload.html")

@index_blueprint.get('/upload_status/<int:id>')
def upload_status(id: int):
    video = Video.query.get(id)

    if not video:
        return abort(404)
    
    return render_template("upload_status.html", video=video)
