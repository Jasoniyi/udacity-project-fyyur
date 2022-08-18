from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String())
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f'<Venue {self.name}>' % self

    @property
    # create a list of dictionaries to be called in the Artist and Venue routes
    def sequence(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description
        }

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return f'<Artist {self.id}>' % self

    @property
    # create a list of dictionaries to be called in the Artist and Venue routes
    def sequence(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website_link': self.website_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description
        }
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'), nullable=False)
