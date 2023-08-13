from flask import render_template, request, flash
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_date

from app import app, db
from models.venue_model import Venue
from models.artist_model import Artist
from models.show_model import Show
from models.genre_model import Genre

from forms import *

#  Shows
#  ----------------------------------------------------------------

@app.route('/V2/shows')
def shows_v2():
  
  statement = select(Show,Venue.name,Artist.name,Artist.image_link).select_from(Venue).join(Show).join(Artist).where(Show.show_datetime > current_date() )
  shows = db.session.execute(statement).all()
  shows_reshaped = list( map( lambda show: {
    "start_time": show[0].show_datetime.isoformat(),
    "artist_id": show[0].artist_id,
    "artist_name": show[2],
    "artist_image_link": show[3],
    "venue_id": show[0].venue_id,
    "venue_name": show[1]}, 
      shows ) )
  return render_template('pages/shows.html', shows=shows_reshaped)

@app.route('/V2/shows/create')
def create_shows_v2():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/V2/shows/create', methods=['POST'])
def create_show_submission_v2():
  form = ShowForm(request.form, meta={'csrf': False})
  
  if not form.validate():
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('forms/new_show.html', form=form)    
  
  artist_id = form.artist_id.data
  venue_id = form.venue_id.data
  start_time = form.start_time.data
  
  with Session(db.engine) as session:
    show = Show( artist_id=artist_id, venue_id=venue_id, show_datetime=datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
    print(show)
    try:
      session.add(show)
      print("Show added")
      session.commit()
      flash('Show was successfully listed!')
    except Exception :
      print(f'show rolled back')
      session.rollback()
      flash('Show could not be listed!', 'error')
      error=True
    finally:
      return shows_v2()
