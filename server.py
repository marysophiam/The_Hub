from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, abort
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, Character, Relationship, Series, User, CharacterSeries, Rating
    # and also other classes once they're worked out?

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "TARDIS"

app.jinja_env.undefined = StrictUndefined


# Eventually links will be the carousel
@app.route('/')
def display_index():
    """Display index template."""

    characters = Character.all()
    series = Series.all()

    return render_template("index.html",
                            characters=characters,
                            series=series)


@app.route('/character/<character_name>')
def display_character(character_name):
    """Display character info template."""

    # character_id = request.args.get("character")
    # character = Character.by_id(character_id)

    # ^^^ Meh, there goes the pretty class method... :(
    # Ask Steve how we can fix this all up.
    # Want all querying done in model file(s) only if possible!

    character = Character.query.filter_by(name=character_name).first()

    if character:
        relationships = character.relationships()
        appearances = character.appearances
        return render_template("character.html",
                                character=character,
                                relationships=relationships,
                                appearances=appearances)
    else:
        abort(404)


@app.route('/series/<series_name>')
def display_series(series_name):
    """Display series info template."""

    # series_id = request.args.get("series")
    series = Series.query.filter_by(name=series_name).first()

    if series:
        characters = series.characters
        return render_template("series.html",
                                series=series,
                                characters=characters)
    else:
        abort(404)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("There's no user by this name.")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password, try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/users/<int:user_id>")
def display_user_info(user_id):
    """Show info about single user by id."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


# What html templates do I still need?
# --base.html + inheritance for all
# --user logout/registration, etc.
# --Splash
# --Voting/Quiz?  # Only if time at very end (not likely right now)


if __name__ == "__main__":
    # Have to set debug=True here, since it has to be True at the point that
    # the DebugToolbarExtension is invoked

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")