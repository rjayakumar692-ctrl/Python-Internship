import pytest

from app import create_app, db
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, username, password='secret123'):
    return client.post('/auth/register', data={
        'username': username, 'email': f'{username}@example.com',
        'password': password, 'password2': password}, follow_redirects=True)


def login(client, username, password='secret123'):
    return client.post('/auth/login', data={'username': username, 'password': password},
                       follow_redirects=True)
