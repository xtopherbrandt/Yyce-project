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
  upcoming_shows_statement = select(Show.show_datetime, Artist.id, Artist.name, Artist.image_link ).select_from(Show).join(Artist).where(Show.show_datetime >= current_date() ).where(Show.venue_id == venue_id)
  upcoming_shows = db.session.execute(upcoming_shows_statement).all()

  past_shows_statement = select(Show.show_datetime, Artist.id, Artist.name, Artist.image_link).select_from(Show).join(Artist).where(Show.show_datetime < current_date() ).where(Show.venue_id == venue_id)
  past_shows = db.session.execute(past_shows_statement).all()
 
  upcoming_shows_reshaped = list( map( lambda show: {
    "start_time": show[0].isoformat(),
    "artist_id": show[1],
    "artist_name": show[2],
    "artist_image_link": show[3]}, 
      upcoming_shows ) )
   
  past_shows_reshaped = list( map( lambda show: {
    "start_time": show[0].isoformat(),
    "artist_id": show[1],
    "artist_name": show[2],
    "artist_image_link": show[3]}, 
      past_shows ) )
  
  venue_information = create_venue_information(venue)
  venue_information["upcoming_shows_count"] = len(upcoming_shows)
  venue_information["upcoming_shows"] = upcoming_shows_reshaped
  venue_information["past_shows_count"] = len(past_shows)
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
  venue_id = 0
  with Session(db.engine) as session:
    genres = []
    for genre_name in genres_input:
      genre = session.query(Genre).filter_by(name=genre_name).all()
      if (len(genre)>0):
        genres.append(genre[0])
    try:    
      venue = Venue( 
                                name=name, 
                                city=city, 
                                state=state, 
                                address=address, 
                                phone=phone, 
                                genres = genres,
                                facebook_link=facebook_link, 
                                image_link=image_link, 
                                website_link=website_link, 
                                seeking_talent=seeking_talent, 
                                seeking_talent_description=seeking_talent_description)
      session.add(venue)
      session.commit()
      venue_id = venue.id
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
  
  return render_template('forms/edit_venue.html', form = form, venue=venue_information)

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
  seeking_talent = True if request.form.get('seeking_talent','') == 'on' else False
  seeking_talent_description = request.form.get('seeking_description','')
  
  genres_input = request.form.getlist('genres')

  with Session(db.engine) as session:
    genres = []
    for genre_name in genres_input:
      genre = session.query(Genre).filter_by(name=genre_name).all()
      if (len(genre)>0):
        genres.append(genre[0])
    try:    
      venue = session.query(Venue).get(venue_id)
      venue.name = name
      venue.city = city
      venue.state = state
      venue.address = address
      venue.phone = phone
      venue.genres = genres
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