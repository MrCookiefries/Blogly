from unittest import TestCase
from app import app
from models import db, User, Tag, Post, PostTag

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Users"""

    def setUp(self):
        """make up sample data"""

        # tag
        tag = Tag(name="Nature")
        db.session.add(tag)
        db.session.commit()

        # user
        user = User(first_name="Bob", last_name="Smith")
        db.session.add(user)
        db.session.commit()

        # post
        post = Post(title="The Great Outdoors", content="Blah, blah.", user_id=user.id)
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()

        self.user = user
        self.post = post
        self.tag = tag
    
    def tearDown(self):
        """clean up the session from fails"""

        db.session.rollback()

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
    
    def test_full_name(self):
        """checks full_name property"""

        user = User(first_name="Bob", last_name="Marley")
        full = user.full_name

        self.assertEqual(full, "Bob Marley")
    
    def test_default_url(self):
        """checks if default url is provided"""

        user = User(first_name="No", last_name="Name")
        url = user.image_url

        self.assertFalse(url)

        db.session.add(user)
        db.session.commit()
        url = user.image_url

        self.assertTrue(url)

    def test_post_author(self):
        """checks if post has an author"""

        self.assertEqual(self.user, self.post.user)
        self.assertEqual(self.user.id, self.post.user_id)
    
    def test_post_tags(self):
        """check if the post has tags"""

        self.assertEqual(self.tag, self.post.tags[0])
        self.assertEqual(self.tag.posts[0], self.post)
    
    def test_default_datetime(self):
        """checks if post has default datetime"""

        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.friendly_date)
