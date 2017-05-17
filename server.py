from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Character, Relationship, Series, User, CharacterSeries, Rating
    # and also other classes once they're worked out?



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "TARDIS"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def display_index():
    """Display index template."""

    characters = Character.query.all()
    series = Series.query.all()

    return render_template("index.html",
                            characters=characters,
                            series=series)


@app.route('/characters')
def display_characters():
    """Display character info template."""

    characters = Character.query.all()

    return render_template("characters.html",
                            characters=characters)



@app.route('/character')
def show_character():
    """Display character info template."""

    character_id = request.args.get("character")

    character = Character.query.filter_by(char_id=character_id).first()

    relationships = Relationship.query.filter((Relationship.char1 == character_id) | (Relationship.char2 == character_id)).all()

    return render_template("character.html",
                            character=character,
                            relationships=relationships)






    ### Need to display: Relationships, Series in









# Need to make html templates, what all will I need?
# -Splash
# -Index
# -Characters/Series (would like to use AJAX to change content w/o redirect);
#   also, display ratings (1-5 stars) on char/series pages


if __name__ == "__main__":
    # Have to set debug=True here, since it has to be True at the point that
    # the DebugToolbarExtension is invoked

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")