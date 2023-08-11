from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from app import db

class Genre(db.Model):
    __tablename__ = 'Genre'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String(120), nullable=True)
    
    def __repr__(self):
        return f'<Genre {self.id} \n \
                name: {self.name} \n \
                description: {self.description} >'