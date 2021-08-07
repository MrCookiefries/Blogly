"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "k36kjgjGAKjl463aGkjg4Gkj344aj#$jf"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.errorhandler(404)
def page_not_found(e):
    """shows 404 not found page"""

    print(e)

    return render_template("404.html"), 404


@app.route("/")
def home_page():
    """shows the home page with recent posts"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5)

    return render_template(
        "home.html",
        posts=posts
    )

@app.route("/users")
def users_page():
    """shows all users"""

    users = User.query.order_by("last_name", "first_name").all()
    # users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template(
        "users.html",
        users=users
    )

@app.route("/tags")
def tags_page():
    """shows all tags"""

    tags = Tag.query.all()

    return render_template(
        "tags.html",
        tags=tags
    )

@app.route("/users/new", methods=["GET", "POST"])
def new_user_page():
    """shows add user form & creates new users"""

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

@app.route("/tags/new", methods=["GET", "POST"])
def new_tag_page():
    """shows the add tag form & creates new tags"""

    posts = Post.query.all()

    if request.method == "GET":
        return render_template(
            "add-tag.html",
            posts=posts
        )
    
    name = request.form.get("name")
    posts = request.form.getlist("posts")

    posts = Post.query.filter(Post.id.in_(posts)).all()
    tag = Tag(name=name)
    tag.posts = posts

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/users/<int:id>/posts/new", methods=["GET", "POST"])
def new_post_page(id):
    """shows the new post form & creates new posts"""

    user = User.query.get_or_404(id)
    tags = Tag.query.all()

    if request.method == "GET":
        return render_template(
            "add-post.html",
            user=user,
            tags=tags
        )
    
    title = request.form.get("title")
    content = request.form.get("content")
    tags = request.form.getlist("tags")
    tags = Tag.query.filter(Tag.id.in_(tags)).all()
    post = Post(title=title, content=content, user_id=id)
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{id}")

@app.route("/users/<int:id>")
def user_page(id):
    """shows details about a user"""

    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template(
        "user.html",
        user=user,
        posts=posts
    )

@app.route("/posts/<int:id>")
def post_page(id):
    """shows details about a post"""

    post = Post.query.get_or_404(id)
    tags = post.tags

    return render_template(
        "post.html",
        post=post,
        tags=tags
    )

@app.route("/tags/<int:id>")
def tag_page(id):
    """shows details about a tag"""

    tag = Tag.query.get_or_404(id)
    posts = tag.posts

    return render_template(
        "tag.html",
        tag=tag,
        posts=posts
    )

@app.route("/users/<int:id>/edit", methods=["GET", "POST"])
def edit_user_page(id):
    """shows the edit user form & saves changes made"""

    user = User.query.get_or_404(id)

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

@app.route("/posts/<int:id>/edit", methods=["GET", "POST"])
def edit_post_page(id):
    """shows the edit post form & saves changes made"""

    post = Post.query.get_or_404(id)
    tags = Tag.query.all()

    if request.method == "GET":
        return render_template(
            "edit-post.html",
            post=post,
            tags=tags,
        )
    
    title = request.form.get("title")
    content = request.form.get("content")
    tags = request.form.getlist("tags")
    tags = Tag.query.filter(Tag.id.in_(tags)).all()

    post.title = title
    post.content = content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{id}")

@app.route("/tags/<int:id>/edit", methods=["GET", "POST"])
def edit_tag_page(id):
    """shows the edit tag form & saves changes made"""

    tag = Tag.query.get_or_404(id)
    posts = Post.query.all()

    if request.method == "GET":
        return render_template(
            "edit-tag.html",
            tag=tag,
            posts=posts
        )
    
    name = request.form.get("name")
    posts = request.form.getlist("posts")
    posts = Post.query.filter(Post.id.in_(posts)).all()
    tag.name = name
    tag.posts = posts

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags")

@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """deletes a user"""

    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/tags/<int:id>/delete", methods=["POST"])
def delete_tag(id):
    """deletes a tag"""

    tag = Tag.query.get_or_404(id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/posts/<int:id>/delete", methods=["POST"])
def delete_post(id):
    """deletes a post"""

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
