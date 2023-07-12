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


#  Artists
#  ----------------------------------------------------------------

@app.route('/V2/artists')
def artists_v2():
  
  artist_statement = select(artist_model.Artist.id, artist_model.Artist.name)
  data = db.session.execute(artist_statement)
  return render_template('pages/artists.html', artists=data)