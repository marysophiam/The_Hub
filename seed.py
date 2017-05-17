import datetime
from sqlalchemy import func

from model import connect_to_db, db, Character, Relationship, Series, User, CharacterSeries, Rating

from server import app


def load_test_characters():

    print 'Characters'

    for line in open("csv/test_data/characters_test.csv"):
        line = line[:-1]
        char_name, actor, char_summary, image_1 = line.split(',')

        character = Character(char_name=char_name,
                              actor=actor,
                              char_summary=char_summary,
                              image_1=image_1)

        db.session.add(character)

    db.session.commit()



def load_test_series():

    print 'Series'

    for line in open("csv/test_data/series_test.csv"):
        line = line[:-1]
        series_name, series_synopsis, series_year, image = line.split(',')

        series = Series(series_name=series_name,
                        series_synopsis=series_synopsis,
                        series_year=series_year,
                        image=image)

        db.session.add(series)

    db.session.commit()


def load_test_relationships():

    print 'Relationships'

    import pdb; pdb.set_trace()
    for line in open("csv/test_data/relationships_test.csv"):
        line = line[:-1]
        char1, char2 = line.split(',')

        character_1 = Character.query.filter_by(char_name=char1).first()
        character_2 = Character.query.filter_by(char_name=char2).first()


        # if not Relationship.query.filter((Relationship.char1==character_1.char_id)&
        #                                  (Relationship.char2==character_2.char_id)).all():

        relationship = Relationship(char1=character_1.char_id,
                                        char2=character_2.char_id)

        db.session.add(relationship)

    db.session.commit()


# Write code for all these, obviously.

# def load_characters():

#     pass


# def load_relationships():

#     pass


# def load_series():

#     pass


# Functions for CharacterSeries, User, Rating?


# THIS ISN'T NEEDED MOST LIKELY, IT'S JUST AN EXAMPLE FROM THE RATINGS LAB

# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_test_characters()
    load_test_series()
    load_test_relationships()

    # Run the functions (loading data, setting value of ids)