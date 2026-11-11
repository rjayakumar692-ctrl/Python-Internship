import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_headers(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "tester", "email": "tester@example.com", "password": "Password123"
    })
    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
