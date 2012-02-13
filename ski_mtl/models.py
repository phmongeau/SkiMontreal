#from ski_mtl import db
from ski_mtl.database import db


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    data = db.Column(db.String())

    def __init__(self, name=None, data=None):
        self.name = name
        self.data = data

    def __repr__(self):
        return '<Track {}>'.format(self.name)
