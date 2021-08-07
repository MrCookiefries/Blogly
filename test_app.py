from unittest import TestCase
from app import app
from models import db, User, Tag, Post, PostTag, pfp_link

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """tests views for Users"""

    def setUp(self):
        """create sample data"""

        # clear out old data
        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()

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
        """clear out session from bad transactions"""

        db.session.rollback()

        PostTag.query.delete()
        Tag.query.delete()
        Post.query.delete()
        User.query.delete()
    
    def test_users_list(self):
        """checks if page is built"""

        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.user.full_name, html)
    
    def test_add_user_redirect(self):
        """checks if a new user form redirects"""

        with app.test_client() as client:
            data = {"first": "Tom", "last": "Brown"}
            res = client.post("/users/new", data=data)

            self.assertEqual(res.status_code, 302)
    
    def test_add_new_user(self):
        """checks if new user is added"""

        with app.test_client() as client:
            data = {"first": "Tom", "last": "Brown"}
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
            res = client.post(f"/users/{self.user.id}/delete")

            self.assertEqual(res.status_code, 302)
    
    def test_delete_user(self):
        """checks if user is deleted"""

        with app.test_client() as client:
            res = client.post(f"/users/{self.user.id}/delete", follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(self.user.full_name, html)
    
    def test_home_page(self):
        """checks if home page is rendered"""

        with app.test_client() as client:
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("The blogging website!", html)
    
    def test_tags_page(self):
        """checks if home page is rendered"""

        with app.test_client() as client:
            res = client.get("/tags")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Tags", html)
    
    def test_post_details_page(self):
        """checks if correct post page is shown"""

        with app.test_client() as client:
            res = client.get(f"/posts/{self.post.id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.post.user.full_name, html)
    
    def test_tag_post(self):
        """checks if correct posts are shown for a tag"""

        with app.test_client() as client:
            res = client.get(f"/tags/{self.tag.id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.tag.posts[0].title, html)
    