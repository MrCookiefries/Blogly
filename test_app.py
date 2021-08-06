from unittest import TestCase
from app import app
from models import db, User, pfp_link

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """tests views for Users"""

    def setUp(self):
        """create sample user"""

        # clear out old users
        User.query.delete()

        user = User(first_name="Bob", last_name="Smith")
        db.session.add(user)
        db.session.commit()

        self.user = user
    
    def tearDown(self):
        """clear out session from bad transactions"""

        db.session.rollback()
    
    def test_users_list(self):
        """checks if page is built"""

        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.full_name, html)
    
    def test_add_user(self):
        """checks if a new user is created"""

        with app.test_client() as client:
            data = {"first": "Tom", "last": "Brown"}
            res = client.post("/users/new", data=data)

            self.assertEqual(res.status_code, 302)

            res = client.post("/users/new", data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Tom Brown", html)
    
    def test_user_details(self):
        """checks if user details page is shown"""

        with app.test_client() as client:
            res = client.get(f"/users/{self.user.id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(pfp_link, html)
            self.assertIn(self.user.image_url, html)
    
    def test_delete_redirect(self):
        """checks if redirect happens"""

        with app.test_client() as client:
            res = client.post("/users/1/delete")

            self.assertEqual(res.status_code, 302)
    
    def test_delete_user(self):
        """checks if user is deleted"""

        with app.test_client() as client:
            res = client.post(f"/users/{self.user.id}/delete", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(self.user.full_name, html)
