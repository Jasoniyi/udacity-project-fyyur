#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from distutils.log import error
import json
from typing_extensions import final
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import collections
from models import *
from config import Config
import sys
from typing_extensions import Required
from flask_wtf.csrf import CSRFProtect
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
csrf = CSRFProtect()
app.config.from_object(Config)
db.init_app(app)
csrf.init_app(app)
# db = SQLAlchemy(app)


migrate = Migrate(app, db)
collections.Callable = collections.abc.Callable

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    venues = Venue.query.all()
    datas = []

    locations = Venue.query.distinct(Venue.city, Venue.state).all()

    for location in locations:
        datas.append({
            'city': location.city,
            'state': location.state,
            'venues': [{
                'id': venue.id,
                'name': venue.name,
                # 'shows': len([show for show in venue.shows if show.start_time > datetime.now()])
            } for venue in venues if
                venue.city == location.city and venue.state == location.state]
        })
    return render_template('pages/venues.html', areas=datas)


@ app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term')
    venues = Venue.query.filter(
        # use ilike to allow caseinsenstive matching
        Venue.name.ilike("%{}%".format(search_term))).all()
    # return number of venues
    venue_count = len(venues)
    response = {
        "count": venue_count,
        "data": [venue.sequence for venue in venues]
    }

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    upcoming_shows = []
    past_shows = []

    getShows = Show.query.all()

    for show in getShows:
        artist = Artist.query.get(show.artist_id)

        if show.start_time <= datetime.now():
            past_shows.append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.start_time)
            })

        if show.start_time > datetime.now():
            upcoming_shows.append({
                "artist_id": show.artist_id,
                "artist_name": artist.name,
                "artist_image_link": artist.image_link,
                "start_time": str(show.start_time)
            })

    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website_link,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@ app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@ app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    new_venue_form = VenueForm(request.form)
    form = new_venue_form
    # TODO: modify data to be the data object returned from db insertion
    if form.validate():
        try:
            new_venue = Venue(
                name=new_venue_form.name.data,
                city=new_venue_form.city.data,
                state=new_venue_form.state.data,
                address=new_venue_form.address.data,
                phone=new_venue_form.phone.data,
                genres=','.join(new_venue_form.genres.data),
                facebook_link=new_venue_form.facebook_link.data,
                image_link=new_venue_form.image_link.data,
                website_link=new_venue_form.website_link.data,
                seeking_talent=new_venue_form.seeking_talent.data,
                seeking_description=new_venue_form.seeking_description.data
            )
            db.session.add(new_venue)
            db.session.commit()

        # on successful db insert, flash success
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')
        except:
            # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
            flash('An error occured. Venue ' +
                  request.form['name'] + ' could not be listed.')
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        return render_template('pages/home.html')
    else:
        print(form.errors)
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        return render_template('pages/home.html')


@ app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        # .one is used to get just one result from d result set
        delete_venue = Venue.query.filter(Venue.id == venue_id).one()
        delete_venue.delete()
        flash('The ' + request.form['name'] + 'has been deleted')

    except:
        if error == True:
            abort(404)
    finally:
        db.session.close()
    return redirect(url_for('index'))

    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    # return None

#  Artists
#  ----------------------------------------------------------------


@ app.route('/artists')
def artists():
    artists = Artist.query.all()
    datas = []

    for artist in artists:
        datas.append({
            'id': artist.id,
            'name': artist.name,
        })

    return render_template('pages/artists.html', artists=datas)


@ app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term')
    artists = Artist.query.filter(
        Artist.name.ilike("%{}%".format(search_term))).all()
    count_of_artist = len(artists)
    response = {
        "count": count_of_artist,
        "data": [a.sequence for a in artists]
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@ app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    error = False

    if error == True:
        abort(400)

    upcoming_shows = []
    past_shows = []

    getShows = Show.query.all()

    for show in getShows:
        venue = Venue.query.get(show.venue_id)

        if show.start_time <= datetime.now():
            past_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time)
            })

        if show.start_time > datetime.now():
            upcoming_shows.append({
                "venue_id": show.venue_id,
                "venue_name": venue.name,
                "venue_image_link": venue.image_link,
                "start_time": str(show.start_time)
            })

    data = {
        'id': artist.id,
        'name': artist.name,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'genres': artist.genres,
        'website_link': artist.website_link,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        "past_shows": past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows),
    }

    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@ app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    update_artists = Artist.query.filter(Artist.id == artist_id).one_or_none()

    artist = update_artists.sequence
    form = ArtistForm(data=artist)
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@ app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    artist = Artist.query.filter_by(id=artist_id).one()

    try:
        artist.name = form.name.data,
        artist.genres = '.'.join(form.genres.data)
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,

        db.session.commit()
        flash(request.form['name'] + ' has been updated')
    except:
        flash('An error occured in updating ' +
              request.form['name'] + 'record')
        db.session.rollback()
    finally:
        db.session.close()
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@ app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    update_venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
    venue = update_venue.sequence
    form = VenueForm(data=venue)

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@ app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    form = VenueForm(request.form)
    venue = Venue.query.filter(Venue.id == venue_id).one()

    try:
        venue.name = form.name.data,
        venue.address = form.address.data,
        venue.genres = '.'.join(form.genres.data),
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.facebook_link = form.facebook_link.data,
        venue.image_link = form.image_link.data,

        db.session.commit()
        flash('venue ' + request.form['name'] + ' has been updated')
    except:
        db.session.rollback()
        flash('An error occured in updating ' +
              request.form['name'] + 'details')
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist_form = ArtistForm(request.form)
    form = ArtistForm()

    # if form.validate():
    try:
        new_artist = Artist(
            name=artist_form.name.data,
            city=artist_form.city.data,
            state=artist_form.state.data,
            phone=artist_form.phone.data,
            genres=','.join(artist_form.genres.data),
            image_link=artist_form.image_link.data,
            facebook_link=artist_form.facebook_link.data,
            website_link=artist_form.website_link.data,
            seeking_venue=artist_form.seeking_venue.data,
            seeking_description=artist_form.seeking_description.data
        )

        db.session.add(new_artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] +
              ' was successfully listed!')
    except:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
        print(sys.exc_info())
    finally:
        db.session.close()
    return render_template('pages/home.html')
    # else:
    #     print(form.errors)
    #     flash('An error occurred. Artist ' +
    #           request.form['name'] + ' could not be listed.')
    #     return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@ app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows = Show.query.all()
    data = []

    for show in shows:
        venue = Venue.query.get(show.venue_id)
        artist = Artist.query.get(show.artist_id)

        data.append({
            'venue_id': show.venue_id,
            'venue_name': venue.name,
            'start_time': str(show.start_time),
            'artist_id': show.artist_id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
        })

    print(data)
    # TODO: replace with real venues data.

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    show_form = ShowForm(request.form)
    form = ShowForm()

    if form.validate():
        try:
            show = Show(
                artist_id=show_form.artist_id.data,
                venue_id=show_form.venue_id.data,
                start_time=show_form.start_time.data,
            )

            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except:
            flash('An error occurred. Show could not be listed.')
            print(sys.exc_info())
        finally:
            db.session.close()
        return render_template('pages/home.html')
    else:
        flash('An error occurred. Show could not be listed.')
        print(sys.exc_info())
        return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
