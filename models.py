"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        u = self
        return f"<User id={u.id} first={u.first_name} last={u.last_name}>"
    
    @property
    def full_name(self):
        """combines names into one string"""

        full_name = f"{self.first_name} {self.last_name}"
        return full_name

