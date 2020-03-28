from flask import abort, g, jsonify, request, url_for

from flaskr.api import api_bp
from flaskr.api.auth import token_auth
from flaskr.api.errors import bad_request
from flaskr.db import db
from flaskr.models import User


@api_bp.route('/users/<int:id_>', methods=['GET'])
@token_auth.login_required
def get_user(id_):
    """
    Get User object with id = `id_`.

    :param int id_: a user ID from the database, actually a primary key.
    :return: Flask `Response` object with added JSON representation of `User` and
    `Content-Type: application/json` HTTP header.
    """
    return jsonify(User.query.get_or_404(id_).to_dict())


@api_bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_all_users():
    """
    Get all users available in database.

    :return: Flask `Response` object with added JSON representation of all `User`
    objects available and `Content-Type: application/json` HTTP header.
    """
    return jsonify(User.to_collection_dict())


@api_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user if not exists.

    :return: Flask `Response` object with added JSON representation of `User` and
    `Content-Type: application/json` HTTP header.
    """
    user_data = request.get_json() or {}
    if any(field not in user_data for field in ('username', 'password')):
        return bad_request('Username and password are mandatory fields')
    if User.query.filter_by(username=user_data['username']).first():
        return bad_request('The user is already exist, please use a different username')
    user = User()
    user.from_dict(user_data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id_=user.id_)
    return response


@api_bp.route('/users/<int:id_>', methods=['PUT'])
@token_auth.login_required
def update_user(id_):
    """
    Update users's attributes.

    :param int id_: a user ID from the database, actually a primary key.
    :return: Flask `Response` object with added JSON representation of `User` and
    `Content-Type: application/json` HTTP header.
    If id of `current_user` != passed id, raise 403 
    """
    if g.current_user.id_ != id_:
        abort(403)
    user = User.query.get_or_404(id_)
    user_data = request.get_json() or {}
    # We should check that new username doesn't conflict with existing users
    if user_data.get('username') != user.username and \
        User.query.filter_by(username=user_data['username']).first():
        return bad_request('Please use a different username')
    user.from_dict(user_data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
