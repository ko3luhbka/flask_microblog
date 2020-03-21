import os
import tempfile
from datetime import datetime

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db
from flaskr.models import Post, User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'SECRET_KEY': 'test',
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
    })

    db_insert_test_data(app)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


def db_insert_test_data(app):
    with app.app_context():
        init_db()
        db = get_db()
        test_user = User(
            username='test',
            password_hash='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
            first_name='TestUserFirstName',
            last_name='TestUserLastName',
        )
        other_user = User(
            username='other',
            password_hash='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79',
            first_name='OtherUserFirstName',
            last_name='OtherUserLastName',
        )
        test_post = Post(
            author_id=1,
            created=datetime.fromisoformat('2020-01-01 00:00:00'),
            title='test title',
            body='test\nbody',
        )
        db.session.add_all((test_user, other_user, test_post))
        db.session.commit()
