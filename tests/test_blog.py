import pytest

from flaskr.db import get_db
from flaskr.models import Post


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2020-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


def test_index_no_posts(app, client, auth):
    with app.app_context():
        db = get_db()
        for post in Post.query.all():
            db.session.delete(post)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert b'There are no posts yet' in response.data


@pytest.mark.parametrize(
    'path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        post = Post.query.get(1)
        post.author_id = 2
        db.session.add(post)
        db.session.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize(
    'path', (
    '/3/update',
    '/3/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    with app.app_context():
        init_post_count = Post.query.count()
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        assert Post.query.count() == init_post_count + 1


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        assert Post.query.get(1).title == 'updated'


@pytest.mark.parametrize(
    'path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        assert Post.query.get(1) is None
