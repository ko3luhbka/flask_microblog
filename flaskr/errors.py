from flask import render_template


def internal_server_error(error):
    return render_template('errors/500.html'), 500


def page_not_found_error(error):
    return render_template('errors/404.html'), 404


def forbidden_error(error):
    return render_template('errors/403.html'), 403
