from uuid import uuid1
from flask import abort, request, Blueprint, render_template, current_app
from database import database
from models import Video, Comment
from redis_queue import (
    transcode,
    redis_queue
)

index_blueprint = Blueprint("index_blueprint", "index_blueprint", url_prefix='/')


# TODO: Make it get not latest video
@index_blueprint.get('/')
def index():
    most_popular_video = Video.query.order_by(Video.id.desc()).first()

    if most_popular_video and most_popular_video.om_url == None:
        most_popular_video = None

    return render_template("index.html", most_popular_video=most_popular_video)


comment_blueprint = Blueprint("comment_blueprint", "comment_blueprint", url_prefix='/comments')


@comment_blueprint.post('/<int:video_id>')
def add_comment(video_id: int):
    comment = Comment(video_id, request.form['comment'])

    database.session.add(comment)
    database.session.commit()

    video = Video.query.get(video_id)

    return render_template("comments.html", comments=video.comments)


upload_blueprint = Blueprint("upload_blueprint", "upload_blueprint", url_prefix='/upload')


@upload_blueprint.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not 'title' and 'description' in request.form or not 'video' in request.files:
            return abort(400)
        
        src = request.files['video']
        src_filepath = f'tmp/{uuid1()}'

        src.save(src_filepath)
        
        video = Video(request.form['title'], request.form['description'])

        database.session.add(video)
        database.session.commit()

        job = transcode.queue(src_filepath, video.id)
        video.rq_id = job.id

        database.session.commit()

        return render_template("upload_post.html", video=video, is_processing=True)
    return render_template("upload.html")


@upload_blueprint.get('/status/<int:id>')
def upload_status(id: int):
    video = Video.query.get(id)

    if not video:
        return abort(404)
    
    job = redis_queue.get_queue("default").fetch_job(video.rq_id)
    return render_template("upload_status.html", video=video, is_processing=not job.result)
