import datetime
from sqlalchemy import func

from model import connect_to_db, db, Character, Relationship, Series, User, CharacterSeries, Rating

from server import app


# Functions here
# ...
# ...
# etc.



if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    # Run the functions (loading data, setting value of ids)