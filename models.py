from database import database
from sqlalchemy.sql import func


class Video(database.Model):
    __tablename__ = "video"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String(100))
    description = database.Column(database.String(500), nullable=True)
    mp4_url = database.Column(database.String(100), nullable=True)
    om_url = database.Column(database.String(100), nullable=True) # for old mobiles (low 3gp format)
    thumbnail_url = database.Column(database.String(100), nullable=True)
    public = database.Column(database.Boolean)
    views = database.Column(database.Integer)
    rq_id = database.Column(database.String(100), nullable=True)
    comments = database.relationship("Comment")

    def __init__(self, title, description, public=False) -> None:
        self.title = title
        self.description = description
        self.public = public
    
    def __repr__(self) -> str:
        return '<Video {0}>'.format(self.title[:17] + '...' if len(self.title) > 20 else self.title)


class Comment(database.Model):
    __tablename__ = "comment"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    video_id = database.Column(database.Integer, database.ForeignKey("video.id"))
    text = database.Column(database.String(500))
    created_date = database.Column(database.DateTime(timezone=True), server_default=func.now())

    def __init__(self, video_id, text) -> None:
        self.video_id = video_id
        self.text = text
    
    def __repr__(self) -> str:
        return '<Video {0}>'.format(self.title[:17] + '...' if len(self.title) > 20 else self.title)
