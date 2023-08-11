from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app import db

class Venue_Genre(db.Model):
    __tablename__ = 'Venue_Genre'

    venue_id = Column(Integer, ForeignKey("Venue.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("Genre.id"), primary_key=True)
    
    def __repr__(self):
        return f'<Venue Venue: {self.venue_id} Genre: {self.genre_id}>'