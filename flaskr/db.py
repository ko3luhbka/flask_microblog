import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def connect_db():
    """Connect to the database"""
    database = sqlite3.connect(
        database=current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    database.row_factory = sqlite3.Row
    return database


def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = connect_db()
    return g.db


def init_db():
    """Initialize database"""
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


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


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
