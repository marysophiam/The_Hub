# Models & db functions for The Hub

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import wikia      # probably don't need this anymore b/c manually entering


db = SQLAlchemy()


#################################################################################
# Model definitions

class Character(db.Model):
    """Character in the Whoniverse."""

    __tablename__ = 'characters'

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_name = db.Column(db.String(50))
    actor = db.Column(db.String(50))
    char_summary = db.Column(db.Text)
    image_1 = db.Column(db.String(100))      # Will be a link to image URL

    # May add another image or 2 later depending on layout
    # Will require dropping db & reseeding
    # Discussed w/ Kiko 5/10 @ 12:15p

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Character char_id=%s char_name=%s>" % (self.char_id, self.char_name)



class Relationship(db.Model):
    """Association table: connects Character table to itself.
       Pairs of characters that have interacted with each other in some way."""

    __tablename__ = 'relationships'

    rel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char1 = db.Column(db.String(50))
    char2 = db.Column(db.String(50))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Relationship rel_id=%s char1=%s char2=%s>" % (self.rel_id, self.char1, self.char2)



class Series(db.Model):
    """A single series (British for "season") of a show in the Whoniverse."""

    __tablename__ = 'series'

    series_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    series_name = db.Column(db.String(50))
    series_synopsis = db.Column(db.Text)
    # changed from DateTime to account for series which occur over multiple years
    series_year = db.Column(db.String(10))
    image = db.Column(db.String(100))      # Will be a link to image URL

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Series series_id=%s series_name=%s>" % (self.series_id, self.series_name)



# TO-DO: Create user account in order to rate/vote on characters
# Need this because: don't want unregistered users to be able to vote;
#   A single user can only rate a character once--otherwise, someone could
#   (for example) upvote Eleven repeatedly, even though Ten is clearly the
#   best Doctor.
# Plus it looks good to have a login/logout/account creation feature.

class User(db.Model):
    """A user of the app who will rate characters."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String(50))
    pswd = db.Column(db.String(20))
    # display_name =    # May or may not use, not really needed for project

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id=%s user_email=%s>" % (self.user_id, self.user_email)



class CharacterSeries(db.Model):
    """Association table between Character & Series."""

    __tablename__ = 'character_series'

    appearance_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    character = db.Column(db.String(50))
    series = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Appearance character=%s series=%s>" % (self.character, self.series)


# Middle table between Character & User
class Rating(db.Model):
    """Rating of a character by a user."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user = db.Column(db.String(50))
    character = db.Column(db.String(50))
    rating = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Rating user=%s character=%s rating=%s>" % (self.user, self.character, self.rating)



##############################################################################
# Helper functions

def connect_to_db(app):
    """ Connect db to Flask app """

    # Configure to use PostgreSQL db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///the_hub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print "Welcome to the Whoniverse."