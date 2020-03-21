from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from sqlalchemy import desc
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.models import Post, User

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Show main app page."""
    db = get_db()
    posts = db.session.query(
        Post.id,
        Post.title,
        Post.body,
        Post.created,
        Post.author_id,
        User.username
    ).join(User).\
        filter(Post.author_id == User.id).\
        order_by(desc(Post.created)).all()

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a blog post and redirect to main page."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    Update `Post` with id = `id` and once it's done redirect to main page.

    :param int id: a post ID to be deleted, database primary key.
    """
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            post.title = title
            post.body = body
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    Delete `Post` with id = `id` and redirect to main page.

    :param int id: a post ID to be deleted, database primary key.
    """
    db = get_db()
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))


def get_post(id, check_author=True):
    """Get `Post` with id = `id` and raise error:
       - 404 if such a post doesn't exist;
       - 403 if current_user's `id` doesn't match post's `id`

    :param boot check_author: check that current user is an author of the post.
    :return: `Post` object.
    """
    post = Post.query.get(id)
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post.author_id != g.user.id:
        abort(403)
    return post
