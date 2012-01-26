from sqlalchemy import Column, Integer, String
from ski_mtl.database import Base

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    data = Column(String())

    def __init__(self, name=None, data=None):
        self.name = name
        self.data = data

    def __repr__(self):
        return '<Track {}>'.format(self.name)

