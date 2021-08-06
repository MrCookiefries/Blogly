"""Blogly application."""

from re import L
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "k36kjgjGAKjl463aGkjg4Gkj344aj#$jf"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():

    return redirect("/users")

@app.route("/users")
def users_page():
    """shows all users"""

    users = User.query.order_by("last_name", "first_name").all()
    # users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template(
        "users.html",
        users=users
    )

@app.route("/users/new", methods=["GET", "POST"])
def new_user_page():
    """shows add user form & creates the new user"""

    if request.method == "GET":
        return render_template("add-user.html")
    
    first = request.form.get("first")
    last = request.form.get("last")
    url = request.form.get("url")
    # handle empty string values for default to kick in
    url = url if url else None
    user = User(first_name=first, last_name=last, image_url=url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:id>")
def user_page(id):
    """shows details about a user"""

    user = User.query.get(id)

    return render_template(
        "user.html",
        user=user
    )

@app.route("/users/<int:id>/edit", methods=["GET", "POST"])
def edit_user_page(id):
    """shows the edit user form & saves changes made"""

    user = User.query.get(id)

    if request.method == "GET":
        return render_template(
            "edit-user.html",
            user=user
        )
    
    first = request.form.get("first")
    last = request.form.get("last")
    url = request.form.get("url")

    user.first_name = first
    user.last_name = last
    user.image_url = url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{id}")

@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """deletes a user"""

    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect("/users")

