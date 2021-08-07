"""seed file to fill up database"""

from models import db, User, Post, Tag
from random import sample, randint
from app import app

# reset the tables
db.drop_all()
db.create_all()

# users - 8
names = [
    ("John", "Doe"),
    ("Oscar", "Arce"),
    ("Sam", "Pound"),
    ("Sarah", "Lynn"),
    ("Bob", "Brown"),
    ("Levi", "Hunter"),
    ("Kelly", "Peters"),
    ("Peter", "Legend")
]

for f, l in names:
    user = User(first_name=f, last_name=l)
    db.session.add(user)

# tags
tags = {"Fun", "Romance", "Scary", "Funny", "Happy", "Sad", "Surprising", "Animals", "Vacation"}

db.session.add_all([Tag(name=t) for t in tags])

db.session.commit()

# posts
posts = [
    ("Brown bears", "Just a little text up in here about brown bears I guess.", 1),
    ("Taco night", "Just a little text up in here about tacos at night I guess.", 2),
    ("Beach party", "Just a little text up in here about a beach party I guess.", 3),
    ("Time I almost died", "Just a little text up in here about how I nearly died I guess.", 4),
    ("Summer love, part 3", "Just a little text up in here about summer love on the third part I guess.", 2),
    ("Cooking with eggs", "Just a little text up in here about cooking with eggs I guess.", 2),
    ("Living by yourself", "Just a little text up in here about living alone I guess.", 1),
    ("Chasing your dreams", "Just a little text up in here about chasing your dreams I guess.", 6)
]

for t, c, i in posts:
    post = Post(title=t, content=c, user_id=i)
    ran_num = randint(1, 4)
    tags = Tag.query.all()
    ran_tags = sample(tags, ran_num)

    for tag in ran_tags:
        post.tags.append(tag)
    
    db.session.add(post)

db.session.commit()

