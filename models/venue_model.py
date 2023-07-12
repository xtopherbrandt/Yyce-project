from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models import show_model
from app import db

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    address = Column(String(120), nullable=False)
    phone = Column(String(120), nullable=False)
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    shows = relationship("Artist", secondary=db.Table("Show"))

    def __repr__(self):
      return f'<Venue {self.id} "{self.name}">'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate