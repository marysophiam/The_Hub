import datetime
from sqlalchemy import func

from model import connect_to_db, db, Character, Relationship, Series, User, CharacterSeries, Rating

from server import app

# TO DO: rename variables to match model.py renamed variables

def load_test_characters():

    for line in open("csv/test_data/characters_test.csv"):
        line = line[:-1]
        name, actor, bio, image = line.split(',')

        character = Character(name=name,
                              actor=actor,
                              bio=bio,
                              image=image)

        db.session.add(character)

    db.session.commit()


def load_test_series():

    for line in open("csv/test_data/series_test.csv"):
        line = line[:-1]
        name, synopsis, date, image = line.split(',')

        series = Series(name=name,
                        synopsis=synopsis,
                        date=date,
                        image=image)

        db.session.add(series)

    db.session.commit()


def load_test_relationships():

    for line in open("csv/test_data/relationships_test.csv"):
        line = line[:-1]
        char1_id, char2_id = line.split(',')

        character_1 = Character.query.filter_by(name=char1_id).first()
        character_2 = Character.query.filter_by(name=char2_id).first()

        relationship = Relationship(char1_id=character_1.char_id,
                                    char2_id=character_2.char_id)

        db.session.add(relationship)

    db.session.commit()



# Write code for all these, obviously.
# Can just rename above functions when data is fully seeded.

# def load_characters():
#   """This will replace load_test_characters()"""

#     pass


# def load_relationships():
#   """This will replace load_test_relationships()"""

#     pass


# def load_series():
#   """This will replace load_test_series()"""

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
    load_test_characters()      # rename later
    load_test_series()          # rename later
    load_test_relationships()   # rename later

    # Run the functions (loading data, setting value of ids)