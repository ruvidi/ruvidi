from database import database


class Video(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String(100))
    description = database.Column(database.String(500), nullable=True)
    mp4_url = database.Column(database.String(100), nullable=True)
    om_url = database.Column(database.String(100), nullable=True) # for old mobiles (low 3gp format)
    public = database.Column(database.Boolean)
    views = database.Column(database.Integer)
    rq_id = database.Column(database.String(100), nullable=True)

    def __init__(self, title, description, public=False) -> None:
        self.title = title
        self.description = description
        self.public = public
    
    def __repr__(self) -> str:
        return '<Video {0}>'.format(self.title[:17] + '...' if len(self.title) > 20 else self.title)
