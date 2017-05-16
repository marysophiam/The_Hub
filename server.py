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