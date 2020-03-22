from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import db


class User(db.Model):
    """Represents blog user database table."""

    id_ = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    last_name = db.Column(db.String(80), unique=False, nullable=False, default='')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
        Create `User` object from provided dictionary `user_dict`.
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
        return '<Post id {0}>'.format(self.id_)

    def to_dict(self):
        """
        Convert `Post` object into dictionary.

        :return: a dictionary with `Post` class attributes.
        """
        post_dict = {
            'id': self.id_,
            'author_id': self.author_id,
            'created': self.created,
            'title': self.title,
            'body': self.body,
        }
        return post_dict

    def from_dict(self, post_dict):
        """
        Create `User` object from provided dictionary `user_dict`.

        :param dict post_dict: a dictionary of `Post` class attributes.
        """
        for field in ('authod_id', 'created', 'title', 'body'):
            if field in post_dict:
                setattr(self, field, post_dict[field])
