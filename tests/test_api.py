import pytest

from flaskr.models import Post, User


@pytest.mark.parametrize('user_id', ('1', '666', ''))
def test_get_user(app, client, user_id):
    with app.app_context():
        user = User.query.get(user_id)
        response = client.get('/api/users/{0}'.format(user_id))
        if user is not None:
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data == user.to_dict()
        else:
            assert response.status_code == 404


def test_get_users(app, client):
    with app.app_context():
        users = User.query.all()
        response = client.get('/api/users')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['users'] == [user.to_dict() for user in users]
        assert json_data['count'] == len(users)


@pytest.mark.parametrize('user_data', (
    {
        'first_name': 'NewUser1FirstName',
        'last_name': 'NewUser1LastName',
        'username': 'new_user1',
        'password': 'pass1',
    },
    {
        'username': 'new_user2',
        'password': 'pass2',
    },
))
def test_create_user_successful(app, client, user_data):
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    with app.app_context():
        db_user = User.query.filter_by(username=user_data['username']).first()
        response_data = response.get_json()
        assert response_data['first_name'] == db_user.first_name == \
            user_data.get('first_name', '')
        assert response_data['last_name'] == db_user.last_name == \
            user_data.get('last_name', '')
        assert response_data['username'] == db_user.username == \
            user_data['username']


def test_create_user_existing(app, client):
    with app.app_context():
        existing_user = User.query.first()
    response = client.post('/api/users', json={
        'username': existing_user.username,
        'password': 'supersecret',
    })
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['message'] == \
        'The user is already exist, please use a different username'


@pytest.mark.parametrize('user_data', (
    {
        'first_name': 'NewUser1FirstName',
        'last_name': 'NewUser1LastName',
        'password': 'pass1',
    },
    {
        'first_name': 'NewUser2FirstName',
        'username': 'new_user2',
    },
))
def test_create_user_bad_fields(app, client, user_data):
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['message'] == \
        'Username and password are mandatory fields'
    with app.app_context():
        assert User.query.filter_by(first_name=user_data['first_name']).first() is None


@pytest.mark.parametrize('user_id, user_data, status_code, err_msg', (
    (1,
    {
        'id_': 666,
        'first_name': 'NewUser2FirstName',
        'username': 'other',
    },
    400,
    'Please use a different username'),
    (1,
    {
        'id_': 666,
        'first_name': 'ChangedFirstName',
        'last_name': 'ChangedLastName',
        'password': 'changed_pass',
        'username': 'new_username',
    },
    200,
    None),
    (1,
    {
        'id_': 1,
        'first_name': 'ChangedFirstName2',
        'last_name': 'ChangedLastName2',
        'password': 'changed_pass2',
        'username': 'test',
    },
    200,
    None),
))
def test_update_user(app, client, user_id, user_data, status_code, err_msg):
    response = client.put('/api/users/{0}'.format(user_id), json=user_data)
    assert response.status_code == status_code
    response_data = response.get_json()
    assert response_data.get('message') == err_msg
    if response.status_code != 200:
        return
    with app.app_context():
        db_user = User.query.get(user_id)
        for key, value in user_data.items():
            if key in ('id_', 'password'):
                continue
            assert response_data[key] == value
            assert getattr(db_user, key) == value


@pytest.mark.parametrize('post_id', ('1', '666', ''))
def test_get_post(app, client, post_id):
    with app.app_context():
        post = Post.query.get(post_id)
        response = client.get('/api/posts/{0}'.format(post_id))
        if post is not None:
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data == post.to_dict()
        else:
            assert response.status_code == 404


def test_get_posts(app, client):
    with app.app_context():
        users_posts = Post.query.join(User).filter(Post.author_id == User.id_).all()
        response = client.get('/api/posts')
        assert response.status_code == 200
        json_data = response.get_json()
        for db_post in users_posts:
            db_post = db_post.to_dict()
            for json_post in json_data['posts']:
                if db_post['id'] != json_post['id']:
                    continue
                assert db_post == json_post
        assert json_data['count'] == len(users_posts)
