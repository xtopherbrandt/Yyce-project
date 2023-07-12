from flask import render_template, request, Response, flash, redirect, url_for
from sqlalchemy import select

from app import app, db
from models import artist_model, venue_model
from forms import *

#  Venues
#  ----------------------------------------------------------------


@app.route('/V2/venues')
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


#  Artists
#  ----------------------------------------------------------------

@app.route('/V2/artists')
def artists_v2():
  
  artist_statement = select(artist_model.Artist.id, artist_model.Artist.name)
  data = db.session.execute(artist_statement)
  return render_template('pages/artists.html', artists=data)

@app.route('/V2/artists/search', methods=['POST'])
def search_artists_v2():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    
  search_term = request.form.get('search_term', '')
  
  artist_search_statement = select(artist_model.Artist.id, artist_model.Artist.name).where(artist_model.Artist.name.ilike( f'%{search_term}%'))
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