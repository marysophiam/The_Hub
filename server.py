from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db,Character, Relationship, Series, User, CharacterSeries, CharacterRating, SeriesRating

import json


app = Flask(__name__)

app.secret_key = "TARDIS"

app.jinja_env.undefined = StrictUndefined


# Eventually links will be the carousel
@app.route('/')
def display_index():
    """Display index template."""

    characters = Character.all()
    series = Series.all()

    data = {"data":[1,2,3,4,5]}
    js_data = json.dumps(data)

    return render_template("index.html",
                            characters=characters,
                            js_data = js_data,
                            series=series)
                            # stuff I did w/ Steve 5/23


# This is the GET method; Dennis said I don't actually have to put "GET" in here
@app.route('/character/<character_name>')
def display_character(character_name):
    """Display character info template."""

    # character_id = request.args.get("character")
    # character = Character.by_id(character_id)

    # ^^^ Meh, there goes the pretty class method... :(
    # Ask Steve how we can fix this all up.
    # Want all querying done in model file(s) only if possible!

    character = Character.query.filter_by(name=character_name).first()

    user_id = session.get("user_id")

    if user_id:
        user_rating = CharacterRating.query.filter_by(
            char_id=character.char_id, user_id=user_id).first()
    else:
        user_rating = None

    rating_scores = [r.score for r in character.character_ratings]
    if rating_scores:
        avg_rating = float(sum(rating_scores)) / len(rating_scores)
        avg_rating = 'Average rating for this character: %.1f' % avg_rating
    # Work out how to display int only if avg isn't a float,
    # float if it is, and to only 1 decimal point
    else:
        avg_rating = "Not yet rated."

    if character:
        f = open(character.bio, 'r')
        char_bio = f.read()
        char_bio = char_bio.decode('utf-8')
        relationships = character.relationships()
        appearances = character.appearances
        return render_template("character.html",
                                character=character,
                                char_bio=char_bio,
                                relationships=relationships,
                                appearances=appearances,
                                user_rating=user_rating,
                                avg_rating=avg_rating)

    else:
        abort(404)


@app.route('/character/<character_name>', methods=['POST'])
def post_character_rating(character_name):

    # Get form variables
    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    character = Character.query.filter_by(name=character_name).first()

    rating = CharacterRating.query.filter_by(user_id=user_id, char_id=character.char_id).first()

    # Come back and re-factor this once the ratings system for both
    # characters & series are in place

    if rating:
        rating.score = score
        # flash("Already rated.")

    else:
        rating = CharacterRating(user_id=user_id, char_id=character.char_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/character/%s" % (character.name))


# GET method
@app.route('/series/<series_name>')
def display_series(series_name):
    """Display series info template."""

    series = Series.query.filter_by(name=series_name).first()

    user_id = session.get("user_id")

    if user_id:
        user_rating = SeriesRating.query.filter_by(
            series_id=series.series_id, user_id=user_id).first()
    else:
        user_rating = None

    rating_scores = [r.score for r in series.series_ratings]
    if rating_scores:
        avg_rating = float(sum(rating_scores)) / len(rating_scores)
        avg_rating = 'Average rating for this series: %.1f' % avg_rating
    # Work out how to display int only if avg isn't a float, float if it is?
    else:
        avg_rating = "Not yet rated."

    if series:
        f = open(series.synopsis, 'r')
        synopsis = f.read()
        synopsis = synopsis.decode('utf-8')
        characters = series.characters
        return render_template("series.html",
                                series=series,
                                synopsis=synopsis,
                                characters=characters,
                                user_rating=user_rating,
                                avg_rating=avg_rating)
    else:
        abort(404)


@app.route('/series/<series_name>', methods=['POST'])
def post_series_rating(series_name):

    score = int(request.form["score"])

    user_id = session.get("user_id")
    if not user_id:
        raise Exception("No user logged in.")

    series = Series.query.filter_by(name=series_name).first()

    rating = SeriesRating.query.filter_by(user_id=user_id, series_id=series.series_id).first()

    # Come back and re-factor this once the ratings system for both
    # characters & series are in place

    if rating:
        rating.score = score
        # flash("Already rated.")

    else:
        rating = SeriesRating(user_id=user_id, series_id=series.series_id, score=score)
        flash("Rating added.")
        db.session.add(rating)

    db.session.commit()

    return redirect("/series/%s" % (series.name))


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
        flash("No user with that email found, please register.")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password, try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome to the Whoniverse.")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/users/%s" % new_user.user_id)


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


@app.route("/characters.json")
def get_info_for_d3():   # Naming?

    json = {"nodes":[], "links":[]}

    characters = Character.all()
    relationships = Relationship.query.all()

    for c in characters:
        node = {}
        node["id"] = c.name
        node["group"] = c.group
        json["nodes"].append(node)

    for r in relationships:

        link = {}
        link["source"] = Character.by_id(r.char1_id).name
        link["target"] = Character.by_id(r.char2_id).name
        link["value"] = str(r.link_est)     # YAAAASSSS IT WORKED
        json["links"].append(link)

        # This did what it was supposed to. But--it doesn't account for the
        # fact that 2 characters may have not met each other in the same series
        # that they both appeared in the Whoniverse. I'm going to have to do
        # this manually (like all the rest of my data) in order to ensure an
        # accurate representation.

        # if Character.first_appears(r.char1_id) > Character.first_appears(r.char2_id):
        #     link["value"] = str(Character.first_appears(r.char1_id))
        # else:
        #     link["value"] = str(Character.first_appears(r.char2_id))

    return jsonify(json)


# Render template for connections.html
@app.route("/visualize")
def show_d3():

    return render_template("connections.html")



# What html templates do I still need?
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