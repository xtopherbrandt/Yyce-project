from flask import render_template, request, Response, flash, redirect, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session, Query

from app import app, db
from models import venue_model
from models.artist_model import Artist
from models.genres_enum import Genres
from forms import *
import json

#  Venues
#  ----------------------------------------------------------------


@app.route('/V2/venues/<int:venue_id>', methods=['GET'])
def show_venue_v2(venue_id):
  venue_information = venue_model.Venue.query.get(venue_id)
  temp_genres = json.loads(venue_information.genres)
  venue_information.genres = [ Genres[genre].value for genre in temp_genres ]
  if venue_information is not None:
    return render_template('pages/show_venue.html', venue=venue_information)
  else :
    flash(f'Could not find a venue with id: {venue_id}')
    return render_template('pages/home.html')
 
@app.route('/V2/venues', methods=['GET'])
def venues_v2():
  data=[]

  cities_statement = select(venue_model.Venue.city, venue_model.Venue.state).distinct().order_by(venue_model.Venue.city)
  
  cities = db.session.execute(cities_statement).all()
  for city in cities:
    venues_in_city_statement = select(venue_model.Venue.id, venue_model.Venue.name).where(venue_model.Venue.city == city[0] ).where(venue_model.Venue.state == city[1] )
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
  
  venue_search_statement = select(venue_model.Venue.id, venue_model.Venue.name).where(venue_model.Venue.name.ilike( f'%{search_term}%'))
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
  name = request.form.get('name','')
  city = request.form.get('city','')
  state = request.form.get('state','')
  address = request.form.get('address','')
  phone = request.form.get('phone','')
  facebook_link = request.form.get('facebook_link','')
  image_link = request.form.get('image_link','')
  website_link = request.form.get('website_link','')
  seeking_talent = True if request.form.get('seeking_talent','') == 'y' else False
  seeking_talent_description = request.form.get('seeking_description','')
    
  genres_input = request.form.getlist('genres')
  genres_json = json.dumps(genres_input)
  
  with Session(db.engine) as session:
    try:    
      venue = venue_model.Venue( 
                                name=name, 
                                city=city, 
                                state=state, 
                                address=address, 
                                phone=phone, 
                                genres = genres_json,
                                facebook_link=facebook_link, 
                                image_link=image_link, 
                                website_link=website_link, 
                                seeking_talent=seeking_talent, 
                                seeking_talent_description=seeking_talent_description)
      session.add(venue)
      session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except :
      session.rollback()
      flash('Venue ' + request.form['name'] + ' could not be listed.')
    finally :
      return render_template('pages/home.html')

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/V2/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue_form_v2(venue_id):
  form = VenueForm()
  session = Session(db.engine)
  venue = session.query(venue_model.Venue).get(venue_id)
  venue.genres = json.loads(venue.genres)
  return render_template('forms/edit_venue.html', form = form, venue=venue)

@app.route('/V2/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_v2(venue_id):
  name = request.form.get('name','')
  city = request.form.get('city','')
  state = request.form.get('state','')
  address = request.form.get('address','')
  phone = request.form.get('phone','')
  facebook_link = request.form.get('facebook_link','')
  image_link = request.form.get('image_link','')
  website_link = request.form.get('website_link','')
  seeking_talent = True if request.form.get('seeking_talent','') == 'y' else False
  seeking_talent_description = request.form.get('seeking_description','')
  
  genres_input = request.form.getlist('genres')
  genres_json = json.dumps(genres_input)
            
  with Session(db.engine) as session:
    try:    
      venue = session.query(venue_model.Venue).get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = genres_json
      venue.facebook_link = facebook_link
      venue.image_link = image_link
      venue.website_link = website_link
      venue.seeking_talent = seeking_talent
      venue.seeking_talent_description = seeking_talent_description
      
      session.add(venue)
      session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except :
      session.rollback()
      flash('Venue ' + request.form['name'] + ' could not be updated.')
    finally :
      return render_template('pages/home.html')
    
@app.route('/V2/venues/<int:venue_id>/delete', methods=['GET'])
@app.route('/V2/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue_v2(venue_id):
  error = False
  with Session(db.engine) as session:
    try:
      venue = session.query(venue_model.Venue).get(venue_id)
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

#  Artists
#  ----------------------------------------------------------------

@app.route('/V2/artists')
def artists_v2():
  
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/V2/artists/<int:artist_id>', methods=['GET'])
def show_artist_v2(artist_id):
  artist = Artist.query.get(artist_id)
  temp_genres = json.loads(artist.genres)
  artist.genres = [ Genres[genre].value for genre in temp_genres ]
  return render_template('pages/show_artist.html', artist=artist)
  
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
  artist.genres = json.loads(artist.genres)
  return render_template('forms/edit_artist.html', form = form, artist=artist)

@app.route('/V2/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_v2(artist_id):
  name = request.form.get('name','')
  city = request.form.get('city','')
  state = request.form.get('state','')
  phone = request.form.get('phone','')
  facebook_link = request.form.get('facebook_link','')
  image_link = request.form.get('image_link','')
  website_link = request.form.get('website_link','')
  seeking_venue = True if request.form.get('seeking_venue','') == 'y' else False
  seeking_description = request.form.get('seeking_description','')
  
  genres_input = request.form.getlist('genres')
  genres_json = json.dumps(genres_input)
            
  with Session(db.engine) as session:
    try:    
      artist = session.query(Artist).get(artist_id)
      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.genres = genres_json
      artist.facebook_link = facebook_link
      artist.image_link = image_link
      artist.website_link = website_link
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      
      session.add(artist)
      session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except :
      session.rollback()
      flash('Artist ' + request.form['name'] + ' could not be updated.')
    finally :
      return render_template('pages/home.html')
    

@app.route('/V2/artists/create', methods=['GET'])
def create_artist_form_v2():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/V2/artists/create', methods=['POST'])
def create_artist_submission_v2():
  name = request.form.get('name','')
  city = request.form.get('city','')
  state = request.form.get('state','')
  phone = request.form.get('phone','')
  facebook_link = request.form.get('facebook_link','')
  image_link = request.form.get('image_link','')
  website_link = request.form.get('website_link','')
  seeking_venue = True if request.form.get('seeking_venue','') == 'y' else False
  seeking_description = request.form.get('seeking_description','')
    
  genres_input = request.form.getlist('genres')
  genres_json = json.dumps(genres_input)
 
  with Session(db.engine) as session:
    try:    
      artist = Artist( 
                      name=name, 
                      city=city, 
                      state=state, 
                      phone=phone, 
                      genres = genres_json,
                      facebook_link=facebook_link, 
                      image_link=image_link, 
                      website_link=website_link, 
                      seeking_venue=seeking_venue, 
                      seeking_description=seeking_description)
      print(artist)
      session.add(artist)
      session.commit()
      print("committed")
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except :
      session.rollback()
      print("rolled back")
      flash('Artist ' + request.form['name'] + ' could not be listed.')
    finally :
      return render_template('pages/home.html')
