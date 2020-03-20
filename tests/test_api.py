import pytest

from flaskr.models import User


@pytest.mark.parametrize('user_id', ('1', '666', ''))
def test_get_user(app, client, user_id):
    with app.app_context():
        user = User.query.get(user_id)
        response = client.get('/api/users/{}'.format(user_id))
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
        'password': 'pass1'
    },
    {
        'username': 'new_user2',
        'password': 'pass2'
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
        'password': 'supersecret'
    })
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['message'] == \
        'The user is already exist, please use a different username'


@pytest.mark.parametrize('user_data', (
    {
        'first_name': 'NewUser1FirstName',
        'last_name': 'NewUser1LastName',
        'password': 'pass1'
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
