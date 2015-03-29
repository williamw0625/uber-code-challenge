# models.py

# # Imports

from app import db

import unicodedata

# # Models


class MovieLocation(db.Model):
    """Encapsulates a movie location."""

    # ## Fields

    # Table columns

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True)
    year = db.Column(db.Integer, index=True)
    location = db.Column(db.String(128))
    fun_fact = db.Column(db.String(512))
    production_company = db.Column(db.String(80), index=True)
    distributor = db.Column(db.String(80), index=True)
    director = db.Column(db.String(80), index=True)
    writer = db.Column(db.String(80), index=True)
    actor_1 = db.Column(db.String(80), index=True)
    actor_2 = db.Column(db.String(80), index=True)
    actor_3 = db.Column(db.String(80), index=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    # ## Methods

    def __repr__(self):
        return '<MovieLocation: {} ({}),'.format(self.title, self.year) + \
            ' written by {}'.format(self.writer) + \
            ' and directed by {}.'.format(self.director) + \
            ' Location: {}>'.format(unicodedata.normalize(
                'NFKD', self.location).encode('ascii', 'ignore'))
