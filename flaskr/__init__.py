import os

from flask import Flask
from flask_migrate import Migrate

from flaskr.errors import (
    page_not_found_error,
    forbidden_error,
    internal_server_error,
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(403, forbidden_error)
    app.register_error_handler(404, page_not_found_error)
    app.register_error_handler(500, internal_server_error)

    database_path = os.path.join(app.instance_path, 'app.db')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=database_path,
        SQLALCHEMY_DATABASE_URI='sqlite:///' + database_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .db import db, init_db_command
    from . import models
    db.init_app(app)
    migrate = Migrate(app, db)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    app.cli.add_command(init_db_command)
    return app
