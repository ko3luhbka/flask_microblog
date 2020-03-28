import base64
import os
from datetime import datetime, timedelta

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import db


class User(db.Model):
    """Represents blog user database table."""

    id_ = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    last_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    api_token = db.Column(db.String(32), unique=True, index=True)
    api_token_expiration = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User(username={}, first_name={}, last_name={})>'.format(
            self.username,
            self.first_name,
            self.last_name,
        )

    def set_password(self, password):
        """Generate password hash and update `password_hash` field.

        :param str password: not hashed user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check that given password's hash matches with one stored in database.

        :param str password: not hashed user's password.
        :return: True if passwords matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_api_token(self, expires_in_sec=3600):
        """
        Set user's token if it doesn't exist or expired, and return it.

        :param int expires_in_sec: a period of time in seconds when the
        token is valid.
        :return: API token string.
        """
        now = datetime.utcnow()
        if self.api_token and self.api_token_expiration > now + timedelta(seconds=60):
            return self.api_token
        self.api_token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.api_token_expiration = now + timedelta(seconds=expires_in_sec)
        db.session.add(self)
        return self.api_token

    def revoke_api_token(self):
        """Make the token be expired."""
        self.api_token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_api_token(token):
        """
        Check if API token exists or expired.
        
        :param str token: REST API token.
        :return: `User` object the `token` belongs to if such exists
        and not expired, `None` otherwise.
        """
        user = User.query.filter_by(api_token=token).first()
        if user is None or user.api_token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        """Convert `User` object to dictionary."""
        user_dict = {
            'id': self.id_,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'post_count': len(self.posts),
        }
        return user_dict

    def from_dict(self, user_dict, new_user=False):
        """
        Populate `User` object with values from dictionary `user_dict`.
        If `new_user` is True, set password as well.

        :param dict user_dict: dictionary containing user attributes.
        :param bool new_user: we don't have `password` field in `User`
        class, but if we create a user, we should set a password.
        """

        for field in ('username', 'first_name', 'last_name'):
            if field in user_dict:
                setattr(self, field, user_dict[field])
        if new_user and 'password' in user_dict:
            self.set_password(user_dict['password'])

    @staticmethod
    def to_collection_dict():
        """
        Create a dictionary of User's dictionaries.

        :return: a dictionary with `User` class attributes.
        """
        users = [user.to_dict() for user in User.query.all()]
        users_collection = {
            'users': users,
            'count': len(users),
        }
        return users_collection


class Post(db.Model):
    """Represents user's blog posts database table."""

    id_ = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id_'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post(id={}, author_id={}, created={}, title={})>'.format(
            self.id_,
            self.author_id,
            self.created,
            self.title,
        )

    def to_dict(self):
        """
        Convert `Post` object into dictionary.

        :return: a dictionary with `Post` class attributes as dictionary and some
        `User` fields under `author` key.
        """
        author = db.session.query(
            User.username,
            User.first_name,
            User.last_name,
        ).filter(self.author_id == User.id_).first()

        post_dict = {
            'id': self.id_,
            'author_id': self.author_id,
            'author': dict(zip(('username', 'first_name', 'last_name'), author)),
            'created': str(self.created),
            'title': self.title,
            'body': self.body,
        }
        return post_dict

    @staticmethod
    def to_collection_dict():
        """
        Create a dictionary of Post's dictionaries.

        :return: a dictionary with `Post` class attributes as dictionary.
        """
        posts = [post.to_dict() for post in Post.query.all()]
        posts_collection = {
            'posts': posts,
            'count': len(posts),
        }
        return posts_collection


    def from_dict(self, post_dict):
        """
        Populate `Post` object with values from dictionary `post_dict`.

        :param dict post_dict: a dictionary of `Post` class attributes.
        """
        for field in ('authod_id', 'created', 'title', 'body'):
            if field in post_dict:
                setattr(self, field, post_dict[field])
