from unittest import TestCase
from app import app
from models import db, User

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Users"""

    def setUp(self):
        """clean up users table"""

        User.query.delete()
    
    def tearDown(self):
        """clean up the session from fails"""

        db.session.rollback()
    
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

