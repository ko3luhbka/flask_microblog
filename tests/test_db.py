import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    # The db object should not change within a request
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # The databese connection should be closed after the request is finished
    with pytest.raises(sqlite3.ProgrammingError) as err:
        db.execute('SELECT 1')

    assert 'Cannot operate on a closed database' in str(err.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Database is initialized' in result.output
    assert Recorder.called


