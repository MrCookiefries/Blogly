"""seed file to fill up database"""

from models import User, db
from app import app

# reset the tables
db.drop_all()
db.create_all()

names = [
    ("John", "Doe"),
    ("Sam", "Pound"),
    ("Sarah", "Lynn"),
    ("Bob", "Brown"),
    ("Oscar", "Smith"),
    ("Levi", "Hunter"),
    ("Kelly", "Peters"),
    ("Peter", "Legend")
]

for f, l in names:
    user = User(first_name=f, last_name=l)
    db.session.add(user)

db.session.commit()
