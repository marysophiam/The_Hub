from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, abort
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Relationship, Series, User, CharacterSeries, Rating
    # and also other classes once they're worked out?

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "TARDIS"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def display_index():
    """Display index template."""

    characters = Character.all()
    series = Series.all()

    return render_template("index.html",
                            characters=characters,
                            series=series)


# Redundant, not needed anymore

# @app.route('/characters')
# def display_characters():
#     """Display character info template."""

#     characters = Character.all()

#     return render_template("characters.html",
#                             characters=characters)


# Still need to display series a character appears in
@app.route('/character')
def display_character():
    """Display character info template."""

    character_id = request.args.get("character")
    character = Character.by_id(character_id)

    if character:
        relationships = character.relationships()
        appearances = character.appearances
        return render_template("character.html",
                                character=character,
                                relationships=relationships,
                                appearances=appearances)
    else:
        abort(404)


@app.route('/series')
def display_series():
    """Display series info template."""

    pass


# What html templates do I still need?
# -Splash
# -Voting/Quiz?


if __name__ == "__main__":
    # Have to set debug=True here, since it has to be True at the point that
    # the DebugToolbarExtension is invoked

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")