import datetime
from sqlalchemy import func

from model import connect_to_db, db, Character, Relationship, Series, User, CharacterSeries, Rating

from server import app

# TO DO: rename variables to match model.py renamed variables

def load_characters():

    for line in open("csv/characters.csv"):
        line = line[:-1]
        name, actor, bio, image = line.split(',')

        character = Character(name=name,
                              actor=actor,
                              bio=bio,
                              image=image)

        db.session.add(character)

    db.session.commit()


def load_series():

    for line in open("csv/series.csv"):
        line = line[:-1]
        name, synopsis, date, image = line.split(',')

        series = Series(name=name,
                        synopsis=synopsis,
                        date=date,
                        image=image)

        db.session.add(series)

    db.session.commit()


def load_relationships():

    for line in open("csv/relationships.csv"):
        line = line[:-1]
        char1_name, char2_name = line.split(',')

        character_1 = Character.query.filter_by(name=char1_name).first()
        character_2 = Character.query.filter_by(name=char2_name).first()

        relationship = Relationship(char1_id=character_1.char_id,
                                    char2_id=character_2.char_id)

        db.session.add(relationship)

    db.session.commit()


def load_appearances():

    for line in open("csv/characterseries.csv"):
        line = line[:-1]
        char_name, series_name = line.split(',')

        character = Character.query.filter_by(name=char_name).first()
        series = Series.query.filter_by(name=series_name).first()

        appearance = CharacterSeries(character=character.char_id,
                                     series=series.series_id)

        db.session.add(appearance)

    db.session.commit()


def load_users():

    for line in open("csv/users.csv"):
        line = line[:-1]
        email, password = line.split(',')

        user = User(email=email,
                    password=password)

        db.session.add(user)

    db.session.commit()


# TO DO:
def load_ratings():

    pass



# THIS ISN'T NEEDED MOST LIKELY, IT'S JUST AN EXAMPLE FROM THE RATINGS LAB
# Unsure though...keeping it here for now just in case...

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
    db.drop_all()
    db.create_all()
    load_characters()
    load_series()
    load_relationships()
    load_appearances()
    load_users()

    # Run the functions (loading data, setting value of ids)