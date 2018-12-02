import os, props
import pytest
from flaskapp import create_app
from flaskapp.db import get_db, push_to_db

with open(os.path.join(os.path.dirname(__file__), 'dummy_data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# using fixtures here to set everything up
@pytest.skip
@pytest.fixture
def app():
    app = create_app({'Testing': True, 'DATABASE': props.SQLALCHEMY_DATABASE_URI})

    with app.app_context():
        push_to_db()
        result = get_db().engine.execute(_data_sql)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_get(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_push_to_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_push_to_db():
        Recorder.called = True

    monkeypatch.setattr('flaskapp.db.push_to_db', fake_push_to_db)
    result = runner.invoke(args=['push_to_db'])
    assert 'Initialized' in result.output
    assert Recorder.called
