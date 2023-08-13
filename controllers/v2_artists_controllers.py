from flask import render_template, request, flash
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_date

from app import app, db
from models.venue_model import Venue
from models.artist_model import Artist
from models.show_model import Show
from models.genre_model import Genre
from models.artist_genre_model import Artist_Genre
from forms import *

#  Artists
#  ----------------------------------------------------------------

@app.route('/V2/artists')
def artists_v2():
  
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/V2/artists/<int:artist_id>', methods=['GET'])
def show_artist_v2(artist_id):
  artist = Artist.query.get(artist_id)
    
  upcoming_shows_reshaped = []
  past_shows_reshaped = []
  
  for show in artist.shows:
    reshaped_show = {
    "start_time": show.show_datetime.isoformat(),
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "venue_image_link": show.venue.image_link
    }
    if show.show_datetime >= datetime.now() :
      upcoming_shows_reshaped.append(reshaped_show)
    else:
      past_shows_reshaped.append(reshaped_show)
  
  artist_information = create_artist_information(artist)
  artist_information["upcoming_shows_count"] = len(upcoming_shows_reshaped)
  artist_information["upcoming_shows"] = upcoming_shows_reshaped
  artist_information["past_shows_count"] = len(past_shows_reshaped)
  artist_information["past_shows"] = past_shows_reshaped
  
  return render_template('pages/show_artist.html', artist=artist_information)

def create_artist_information(artist):
  
  genres_reshaped = list( map( lambda genre: genre.name, artist.genres))
    
  return {
    "id": artist.id,
    "name": artist.name,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "image_link": artist.image_link,
    "facebook_link": artist.facebook_link,
    "website_link": artist.website_link,
    "genres": genres_reshaped,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description
  }
  
@app.route('/V2/artists/search', methods=['POST'])
def search_artists_v2():
    
  search_term = request.form.get('search_term', '')
  
  artist_search_statement = select(Artist.id, Artist.name).where(Artist.name.ilike( f'%{search_term}%'))
  search_results = db.session.execute(artist_search_statement)
  count = 0
  data = []
  for artist in search_results.all():
    data.append({
      "id": artist[0],
      "name": artist[1],
      "num_upcoming_shows": 0
    })
    count += 1
    
  response={
    "count": count,
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/V2/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist_form_v2(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist_information = create_artist_information(artist)
  
  form.state.default = artist_information['state']
  form.seeking_venue.default = artist_information['seeking_venue']
  form.genres.default = artist_information['genres'] 
  form.process()
  
  return render_template('forms/edit_artist.html', form = form, artist=artist_information)

@app.route('/V2/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_v2(artist_id):
  form = ArtistForm(request.form, meta={'csrf': False})
  
  if not form.validate():
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('forms/new_artist.html', form=form)    

  name = form.name.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  website_link = form.website_link.data
  seeking_venue = form.seeking_venue.data
  seeking_description = form.seeking_description.data
  genres_input = form.genres.data
            
  with Session(db.engine) as session:

    try:    
      genres = []
      for genre_name in genres_input:
        genre = session.query(Genre).filter_by(name=genre_name).first()
        
        if (genre is None):
          new_genre = Genre(name=genre_name)
          db.session.add(new_genre)
          db.session.commit()
          genres.append(new_genre)
        else:
          genres.append(genre)

      artist = session.query(Artist).get(artist_id)

      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.facebook_link = facebook_link
      artist.image_link = image_link
      artist.website_link = website_link
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      artist.genres = []

      session.add(artist)
      session.commit()

      for genre in genres:
        artist_genre = Artist_Genre(artist_id=artist.id, genre_id=genre.id)
        db.session.add(artist_genre)
        db.session.commit()

      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except :
      session.rollback()
      flash('Artist ' + request.form['name'] + ' could not be updated.')
    finally :
      return show_artist_v2(artist_id)
    

@app.route('/V2/artists/create', methods=['GET'])
def create_artist_form_v2():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/V2/artists/create', methods=['POST'])
def create_artist_submission_v2():
  form = ArtistForm(request.form, meta={'csrf': False})
  
  if not form.validate():
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('forms/new_artist.html', form=form)    

  name = form.name.data
  city = form.city.data
  state = form.state.data
  phone = form.phone.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  website_link = form.website_link.data
  seeking_venue = form.seeking_venue.data
  seeking_description = form.seeking_description.data
  genres_input = form.genres.data
 
  with Session(db.engine) as session:
    try:    
      genres = []
      for genre_name in genres_input:
        genre = session.query(Genre).filter_by(name=genre_name).first()
        
        if (genre is None):
          new_genre = Genre(name=genre_name)
          db.session.add(new_genre)
          db.session.commit()
          genres.append(new_genre)
        else:
          genres.append(genre)

      artist = session.query(Artist).get(artist_id)

      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.facebook_link = facebook_link
      artist.image_link = image_link
      artist.website_link = website_link
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      artist.genres = []

      session.add(artist)
      session.commit()

      for genre in genres:
        artist_genre = Artist_Genre(artist_id=artist.id, genre_id=genre.id)
        db.session.add(artist_genre)
        db.session.commit()
        
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except :
      session.rollback()
      print("rolled back")
      flash('Artist ' + request.form['name'] + ' could not be listed.')
    finally :
      return show_artist_v2(artist.id)
    
@app.route('/V2/artists/<int:artist_id>/delete', methods=['GET'])
@app.route('/V2/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist_v2(artist_id):
  error = False
  with Session(db.engine) as session:
    try:
      artist = session.query(Artist).get(artist_id)
      session.delete(artist)
      session.commit()
      print (f'Artist {artist.name} deleted')
      flash(f'Artist {artist.name} was successfully deleted.')
    except:
      error = True
      flash(f'Artist {artist.name} could not be deleted.')
      session.rollback()
      print ('delete rolled back')
    finally :
      if error :
        AssertionError()
      else:
        return render_template('pages/home.html')

  return None
