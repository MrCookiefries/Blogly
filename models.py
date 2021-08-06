"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# Image taken on August 5th, 2021
# https://www.seekpng.com/ks/profile-icon/
pfp_link = "https://www.seekpng.com/png/small/41-410093_circled-user-icon-user-profile-icon-png.png"

def connect_db(app):
    """connects app to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users table model"""
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    first_name = db.Column(
        db.String(15),
        nullable=False
    )

    last_name = db.Column(
        db.String(15),
        nullable=False
    )

    image_url = db.Column(
        db.String,
        default=pfp_link
    )

    # can have many posts
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"<User id={u.id} first={u.first_name} last={u.last_name}>"
    
    @property
    def full_name(self):
        """combines names into one string"""

        full_name = f"{self.first_name} {self.last_name}"
        return full_name

class Post(db.Model):
    """Posts table model"""
    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(50),
        nullable=False,
    )

    content = db.Column(
        db.String,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now
    )

    # has one author
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        p = self
        return f"<Post id={p.id} user_id={p.user_id} title={p.title}>"

    @property
    def friendly_date(self):
        """formats date into a nice format"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
