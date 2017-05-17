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
    name = db.Column(db.String(50))
    actor = db.Column(db.String(50))
    bio = db.Column(db.Text)
    image = db.Column(db.String(100))   # Will be a link to image URL

    @classmethod
    def by_id(cls, char_id):
        q = cls.query.filter_by(char_id=char_id)
        c = q.first()
        return c

    @classmethod
    def by_ids(cls, char_ids):
        q = cls.query.filter(cls.char_id.in_(char_ids))
        return q.all()
   
    @classmethod
    def all(cls):
        q = cls.query
        return q.all()

    @classmethod
    def new(cls, name, actor, summary, image):
        # c = create obj
        # c.insert()
        return c

    def relationships(self):
        # find relationships

        # GO BACK AND PLAY AROUND WITH THIS WHEN YOU HAVE A LITTLE TIME
        # import pdb; pdb.set_trace()

        q = Relationship.query
        filter_rels = q.filter((Relationship.char1_id == self.char_id) | 
                 (Relationship.char2_id == self.char_id)).all()
        
        # build list of char_id's
        char_ids = []
        for rel in filter_rels:
            char_ids.extend((rel.char1_id, rel.char2_id))
        char_ids = set(char_ids)

        # look up characters    # characters that self is related to + self
        chars = Character.by_ids(char_ids)
        # remove myself
        chars = [c for c in chars if c.char_id != self.char_id]

        return chars

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Character char_id=%s name=%s>" % (self.char_id, self.name)


class Relationship(db.Model):
    """Association table: connects Character table to itself.
       Pairs of characters that have interacted with each other in some way."""

    __tablename__ = 'relationships'

    rel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char1_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    char2_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Relationship rel_id=%s char1_id=%s char2_id=%s>" % (self.rel_id, self.char1_id, self.char2_id)


class Series(db.Model):
    """A single series (British for "season") of a show in the Whoniverse."""

    __tablename__ = 'series'

    # TO DO: change some variable names to make more sense/for ease of reading
    # name TO title
    # synopsis TO synopsis
    # date TO date

    series_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    synopsis = db.Column(db.Text)
    # changed from DateTime to account for series which occur over multiple years
    date = db.Column(db.String(10))
    image = db.Column(db.String(100))   # Will be a link to image URL

    @classmethod
    def all(cls):
        q = cls.query
        return q.all()

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Series series_id=%s name=%s>" % (self.series_id, self.name)


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
    character = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    series = db.Column(db.Integer, db.ForeignKey('series.series_id'))

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