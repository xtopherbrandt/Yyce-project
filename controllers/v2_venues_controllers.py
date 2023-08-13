from flask import render_template, request, flash
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_date

from datetime import datetime

from app import app, db
from models.venue_model import Venue
from models.artist_model import Artist
from models.show_model import Show
from models.genre_model import Genre
from models.venue_genre_model import Venue_Genre
from forms import *

#  Venues
#  ----------------------------------------------------------------


@app.route('/V2/venues/<int:venue_id>', methods=['GET'])
def show_venue_v2(venue_id):
  venue = Venue.query.get(venue_id)
  
  if venue is None:
    return render_template('errors/404.html'), 404
  
  print(venue)
    
  upcoming_shows_reshaped = []
  past_shows_reshaped = []
  
  for show in venue.shows:
    reshaped_show = {
    "start_time": show.show_datetime.isoformat(),
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link
    }
    if show.show_datetime >= datetime.now() :
      upcoming_shows_reshaped.append(reshaped_show)
    else:
      past_shows_reshaped.append(reshaped_show)
    
  venue_information = create_venue_information(venue)
  venue_information["upcoming_shows_count"] = len(upcoming_shows_reshaped)
  venue_information["upcoming_shows"] = upcoming_shows_reshaped
  venue_information["past_shows_count"] = len(past_shows_reshaped)
  venue_information["past_shows"] = past_shows_reshaped

  if venue is not None:
    return render_template('pages/show_venue.html', venue=venue_information)
  else :
    flash(f'Could not find a venue with id: {venue_id}')
    return render_template('pages/home.html')

def create_venue_information(venue):
  
  genres_reshaped = list( map( lambda genre: genre.name, venue.genres))
    
  return {
    "id": venue.id,
    "name": venue.name,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "image_link": venue.image_link,
    "facebook_link": venue.facebook_link,
    "website_link": venue.website_link,
    "genres": genres_reshaped,
    "seeking_talent": venue.seeking_talent,
    "seeking_talent_description": venue.seeking_talent_description
  }
  
@app.route('/V2/venues', methods=['GET'])
def venues_v2():
  data=[]

  cities_statement = select(Venue.city, Venue.state).distinct().order_by(Venue.city)
  
  cities = db.session.execute(cities_statement).all()
  for city in cities:
    venues_in_city_statement = select(Venue.id, Venue.name).where(Venue.city == city[0] ).where(Venue.state == city[1] )
    venues = db.session.execute(venues_in_city_statement)
    city_data_json = {
      "city": city[0],
      "state": city[1],
      "venues": []
    }

    for venue in venues:
      city_data_json["venues"].append({
        "id": venue[0],
        "name": venue[1],
        "num_upcoming_shows": 0 #requires a many-many relationship with Artists
      })
    data.append( city_data_json )      
  return render_template('pages/venues.html', areas=data)


@app.route('/V2/venues/search', methods=['POST'])
def search_venues_v2():
  
  search_term = request.form.get('search_term', '')
  
  venue_search_statement = select(Venue.id, Venue.name).where(Venue.name.ilike( f'%{search_term}%'))
  search_results = db.session.execute(venue_search_statement)
  count = 0
  data = []
  for venue in search_results.all():
    data.append({
      "id": venue[0],
      "name": venue[1],
      "num_upcoming_shows": 0
    })
    count += 1
    
  response={
    "count": count,
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/V2/venues/create', methods=['GET'])
def create_venue_form_v2():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/V2/venues/create', methods=['POST'])
def create_venue_submission_v2():
  form = VenueForm(request.form, meta={'csrf': False})
  
  if not form.validate():
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)    
  
  name = form.name.data
  city = form.city.data
  state = form.state.data
  address = form.address.data
  phone = form.phone.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  website_link = form.website_link.data
  seeking_talent = form.seeking_talent.data
  seeking_talent_description = form.seeking_description.data
  genres_input = form.genres.data
  venue_id = 0
  
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
        
      venue = session.query(Venue).get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = []
      venue.facebook_link = facebook_link
      venue.image_link = image_link
      venue.website_link = website_link
      venue.seeking_talent = seeking_talent
      venue.seeking_talent_description = seeking_talent_description

      session.add(venue)
      session.commit()
      
      for genre in genres:
        venue_genre = Venue_Genre(venue_id=venue.id, genre_id=genre.id)
        db.session.add(venue_genre)
        db.session.commit()
        
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except :
      session.rollback()
      flash('Venue ' + request.form['name'] + ' could not be listed.')
    finally :
      return show_venue_v2(venue_id)

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/V2/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue_form_v2(venue_id):
  form = VenueForm()
  session = Session(db.engine)
  venue = session.query(Venue).get(venue_id)
  venue_information = create_venue_information(venue)

  form.state.default = venue_information['state']
  form.seeking_talent.default = venue_information['seeking_talent']
  form.genres.default = venue_information['genres'] 
  form.process()
  return render_template('forms/edit_venue.html', form = form, venue=venue_information)

@app.route('/V2/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_v2(venue_id):
  form = VenueForm(request.form, meta={'csrf': False})
  
  if not form.validate():
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)    

  name = form.name.data
  city = form.city.data
  state = form.state.data
  address = form.address.data
  phone = form.phone.data
  facebook_link = form.facebook_link.data
  image_link = form.image_link.data
  website_link = form.website_link.data
  seeking_talent = form.seeking_talent.data
  seeking_talent_description = form.seeking_description.data
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
        
      venue = session.query(Venue).get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = []
      venue.facebook_link = facebook_link
      venue.image_link = image_link
      venue.website_link = website_link
      venue.seeking_talent = seeking_talent
      venue.seeking_talent_description = seeking_talent_description

      session.add(venue)
      session.commit()
      
      for genre in genres:
        venue_genre = Venue_Genre(venue_id=venue.id, genre_id=genre.id)
        db.session.add(venue_genre)
        db.session.commit()
              
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except :
      session.rollback()
      flash('Venue ' + request.form['name'] + ' could not be updated.')
    finally :
      return show_venue_v2(venue_id)
    
@app.route('/V2/venues/<int:venue_id>/delete', methods=['GET'])
@app.route('/V2/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue_v2(venue_id):
  error = False
  with Session(db.engine) as session:
    try:
      venue = session.query(Venue).get(venue_id)
      session.delete(venue)
      session.commit()
      print (f'Venue {venue.name} deleted')
      flash(f'Venue {venue.name} was successfully deleted.')
    except:
      error = True
      flash(f'Venue {venue.name} could not be deleted.')
      session.rollback()
      print ('delete rolled back')
    finally :
      if error :
        AssertionError()
      else:
        return render_template('pages/home.html')

  return None
