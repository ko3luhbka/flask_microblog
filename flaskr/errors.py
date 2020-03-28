from flask import request, render_template
from flaskr.api.errors import error_response as api_error_response


def wants_json_response():
    """
    Check if client's `application/json mimetype
    has higher priority than `text/html.

    :return: `True` if client prefers JSON, False otherwise.
    """
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


def internal_server_error(error):
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500


def page_not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


def forbidden_error(error):
    if wants_json_response():
        return api_error_response(403)
    return render_template('errors/403.html'), 403
