from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String, Boolean
from sqlalchemy.orm import relationship
from models import artist_genre_model
from app import db

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String(120), nullable=False)
    state = Column(String(120), nullable=False)
    phone = Column(String(120), nullable=False)
    genres = relationship("Genre", secondary=db.Table("Artist_Genre"))
    image_link = Column(String(500))
    facebook_link = Column(String(120))
    website_link = Column(String(120))
    seeking_venue = Column(Boolean(), nullable=False)
    seeking_description = Column(String(500))
    shows = relationship('Show', backref='artist', lazy='joined', cascade="all, delete")
    
    def __repr__(self):
      return f'<Artist {self.id} \n \
                name: {self.name} \n \
                city: {self.city} \n \
                state: {self.state} \n \
                phone: {self.phone} \n \
                genres: {self.genres} \n \
                image link: {self.image_link} \n \
                facebook link: {self.facebook_link} \n \
                website link: {self.website_link} \n \
                seeking venue: {self.seeking_venue} \n \
                seeking description: {self.seeking_description} >'
