import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_migrate import Migrate

from config import Config
from flaskr.errors import forbidden_error, internal_server_error, page_not_found_error


def create_app(test_config=None):
    app = Flask(__name__)
    app.register_error_handler(403, forbidden_error)
    app.register_error_handler(404, page_not_found_error)
    app.register_error_handler(500, internal_server_error)

    app.config.from_object(Config)

    if test_config is not None:
        app.config.from_mapping(test_config)

    from flaskr.db import db, init_db_command

    db.init_app(app)
    migrate = Migrate(app, db)
    from flaskr import auth
    app.register_blueprint(auth.bp)
    from flaskr import blog
    from flaskr import models
    app.register_blueprint(blog.bp)
    from flaskr.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.add_url_rule('/', endpoint='index')
    app.cli.add_command(init_db_command)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            filename='logs/flaskr.log',
            maxBytes=10240,
            backupCount=10,
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Flaskr startup')
    return app
