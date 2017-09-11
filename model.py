# Models & db functions for The Hub

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import wikia      # probably don't need this anymore b/c manually entering


db = SQLAlchemy()


# TO DO:
# Separate models into discrete files (this file is getting really long)

########################################################################
# Model definitions

class Character(db.Model):
    """Character in the Whoniverse."""

    __tablename__ = 'characters'

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    # 1 = Doctor Regeneration, 2 = Companion,
    # 3 = Jack (fixed point in time & space), 4 = Torchwood
    group = db.Column(db.Integer)
    actor = db.Column(db.String(50))
    bio = db.Column(db.Text)
    image = db.Column(db.String(100))   # Will be a link to image URL


    @classmethod
    def all(cls):
        q = cls.query
        return q.all()

    # Combine by_id & by_ids in future refactoring?

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
    def by_name(cls, name):
        q = cls.query.filter_by(name=name)
        c = q.first()
        return c

    # TO DO
    # This will be used in display_character(), post_character_rating(), where else?

    # @classmethod
    # def filter_by():

    #     pass

    # For future feature to allow users to add a character to db
    # @classmethod
    # def new(cls, name, actor, bio, image):
    #     # c = create obj
    #     # c.insert()
    #     return c

    # Is this a @staticmethod ? (think so...)
    def relationships(self):
        # find relationships

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


    appearances = db.relationship("Series",
                                  secondary="character_series",
                                  backref="characters")


    # Not needed at present: entering manually because a link between characters
    # isn't necessarily established right when a character enters the timeline.

    # @staticmethod
    # def first_appears(char_id):
    #     """Determine first series a character appears in."""

    #     series_in = Character.by_id(char_id).appearances
    #     series_set = {s.chron_order for s in series_in}
    #     first = min(series_set)

    #     return first


    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Character char_id=%s name=%s>" % (self.char_id, self.name)


class Relationship(db.Model):
    """Middle table: connects Character table to itself.
       Pairs of characters that have interacted with each other in some way."""

    __tablename__ = 'relationships'

    rel_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char1_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    char2_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    # TO DO: Need to reverse order in .csv file for the D3 slider
    # Threshold for D3 slider
    threshold = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Relationship rel_id=%s char1_id=%s char2_id=%s>" % (self.rel_id, self.char1_id, self.char2_id)


class Series(db.Model):
    """A single series (British for "season") of a show in the Whoniverse."""

    __tablename__ = 'series'

    series_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    synopsis = db.Column(db.Text)
    # changed from DateTime to account for series which occur over multiple years
    date = db.Column(db.String(10))
    chron_order = db.Column(db.Integer) # not needed anymore, remove
    image = db.Column(db.String(100))   # Will be a link to image URL

    @classmethod
    def all(cls):
        q = cls.query
        return q.all()

    @classmethod
    def by_id(cls, series_id):
        q = cls.query.filter_by(series_id=series_id)
        s = q.first()
        return s

    # Added 5/28, not used yet
    @classmethod
    def by_name(cls, name):
        q = cls.query.filter_by(name=name)
        s = q.first()
        return s

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Series series_id=%s name=%s>" % (self.series_id, self.name)


class CharacterSeries(db.Model):
    """Association table between Character & Series."""

    __tablename__ = 'character_series'

    appearance_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # PrimaryKeyConstraint
    character = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    series = db.Column(db.Integer, db.ForeignKey('series.series_id'))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Appearance character=%s series=%s>" % (self.character, self.series)


class User(db.Model):
    """A user of the app who will rate characters."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    # display_name =    # May or may not use, not really needed for project

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


# Middle table between Character & User
class CharacterRating(db.Model):
    """Rating of a character by a user."""

    __tablename__ = 'character_ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    char_id = db.Column(db.Integer, db.ForeignKey('characters.char_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("character_ratings", order_by=rating_id))

    # Define relationship to character
    character = db.relationship("Character",
                            backref=db.backref("character_ratings", order_by=rating_id))


    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Rating rating_id=%s character=%s user=%s score=%s>" % (self.rating_id, self.character, self.user, self.score)


# Middle table between Series & User
class SeriesRating(db.Model):
    """Rating of a character by a user."""

    __tablename__ = 'series_ratings'

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.series_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    score = db.Column(db.Integer)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("series_ratings", order_by=rating_id))

    # Define relationship to character
    series = db.relationship("Series",
                            backref=db.backref("series_ratings", order_by=rating_id))


    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Rating rating_id=%s series=%s user=%s score=%s>" % (self.rating_id, self.series, self.user, self.score)


#############################################################################
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