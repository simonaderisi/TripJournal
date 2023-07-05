from tripJournal import db

class Post(db.Model):
    __bind_key__ = 'scrittura'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(5000))
    images = db.Column(db.String(1000))
    date = db.Column(db.DateTime)

    def __init__(self, title, author, description, images, date):
        self.title = title
        self.author = author
        self.description = description
        self.images = images
        self.date = date


