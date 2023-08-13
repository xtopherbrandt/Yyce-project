from datetime import datetime
from flask_wtf import  FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, URL
from models.genres_enum import Genres
from models.state_enum import States
import re

def is_valid_phone_number(number):
    """ Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator

    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]
    """
    regex = re.compile(r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    return regex.match(number)

def validate_phone(self, field):
    if not is_valid_phone_number(field.data):
        raise ValidationError('Invalid phone.')
        
def validate_state(self, field):
    if field.data not in States.list():
        raise ValidationError('Invalid state.')
        
def validate_genres(self, field):
    if field.data not in Genres.list():
        raise ValidationError('Invalid state.')

def validate(self, **kwargs):
    # `**kwargs` to match the method's signature in the `FlaskForm` class.
    return super(VenueForm, self).validate(**kwargs)
    
class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), validate_state],
        choices=[ (state.value) for state in States ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), validate_genres],
        choices= [ (genre.value) for genre in Genres ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'website_link', validators=[URL()]
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired(), validate_state],
        choices=[ (state.value) for state in States ]
    )
    phone = StringField(
        'phone', validators=[validate_phone]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), validate_genres],
        choices= [ (genre.value) for genre in Genres ]
     )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'website_link', validators=[URL()]
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

