from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app import db

class Show(db.Model):
    __tablename__ = 'Show'

    venue_id = Column(Integer, ForeignKey("Venue.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("Artist.id"), primary_key=True)
    show_datetime = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Show Venue: {self.venue_id} Artist: {self.artist_id} Show Time: {self.show_datetime}>'
 