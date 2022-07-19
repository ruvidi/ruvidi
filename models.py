from database import database


class Video(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    