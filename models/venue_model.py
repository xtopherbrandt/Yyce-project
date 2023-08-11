from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship
from models import show_model, venue_genre_model
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
    website_link = Column(String(120))
    genres = relationship("Genre", secondary=db.Table("Venue_Genre"))
    seeking_talent = Column(Boolean(), nullable=False)
    seeking_talent_description = Column(String(500))
    shows = relationship("Artist", secondary=db.Table("Show"))

    def __repr__(self):
      return f'<Venue {self.id} \n \
                name: {self.name} \n \
                city: {self.city} \n \
                state: {self.state} \n \
                address: {self.address} \n \
                phone: {self.phone} \n \
                genres: {self.genres} \n \
                image link: {self.image_link} \n \
                facebook link: {self.facebook_link} \n \
                website link: {self.website_link} \n \
                seeking talent: {self.seeking_talent} \n \
                seeking description: {self.seeking_talent_description}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate