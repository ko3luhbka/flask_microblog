import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Check this out for more details:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#using-custom-metadata-and-naming-conventions
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}
metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


def get_db():
    """
    Get database connection.

    :return: a database object stored in Flask's `g`.
    """
    if 'db' not in g:
        g.db = db
    return g.db


def init_db():
    """Create all database tables."""
    db.create_all()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Command-line command for creating all database tables."""
    init_db()
    click.echo('Database is initialized')
