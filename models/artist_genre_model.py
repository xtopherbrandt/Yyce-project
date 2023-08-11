from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from models import genre_model
from app import db

class Artist_Genre(db.Model):
    __tablename__ = 'Artist_Genre'

    artist_id = Column(Integer, ForeignKey("Artist.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("Genre.id"), primary_key=True)
    
    def __repr__(self):
        return f'<Artist Artist: {self.artist_id} Genre: {self.genre_id}>'