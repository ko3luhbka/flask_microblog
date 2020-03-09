import click
from flask import g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = db
    return g.db


def init_db():
    """Initialize database"""
    db.create_all()

def close_db(error=None):
    """Close DB connection if exists"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing database and create new tables"""
    init_db()
    click.echo('Database is initialized')
