from flask import g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from flaskr.api.errors import error_response
from flaskr.models import User


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """
    Check user's password.

    :param str username: username.
    :param str password: not hashed password.
    :return: `True` if user `username` exists and his password
    matches with hashed`password`, `False` otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    """Just return '401 Unauthorized' error."""
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_api_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return error_response(401)
